import numba
from antlr4 import *
from llvmlite.ir import IRBuilder
from llvmlite.ir import *

if __name__ is not None and "." in __name__:
    from .SmallCParser import SmallCParser
else:
    from SmallCParser import SmallCParser

# generator

from SmallCVisitor import SmallCVisitor


class GeneratorVisitor(SmallCVisitor):

    def __init__(self, output_file=None):
        super(SmallCVisitor, self).__init__()
        self.Module = Module(name=__file__)
        self.Builder = None
        self.function = None
        self.NamedValues = dict()
        self.counter = 0
        self.loop_stack = []
        self.cond_stack = []
        self.var_stack = []
        self.cur_decl_type = None

        self.indentation = 0
        self.function_dict = dict()
        self.error_queue = list()
        self.output_file = output_file

    def print(self):
        if not self.output_file:
            print(self.Module)
        else:
            self.output_file.write(self.Module)

    def error(self, info):
        print("Error: ", info)
        return 0

    def toBool(self, value):
        zero = Constant(self.getType('bool'), 0)
        return self.Builder.icmp_signed('!=', value, zero)

    def getVal_of_expr(self, expr):
        var_map = self.var_stack[-1]
        temp = self.visit(expr)
        if isinstance(temp, Constant) or isinstance(temp, CallInstr) or isinstance(temp,LoadInstr) or isinstance(temp,Instruction):
            value = temp
        else:
            temp_ptr = self.getVal_local(temp.IDENTIFIER().getText())['ptr']
            if temp.array_indexing():
                index = self.getVal_of_expr(temp.array_indexing().expr())
                temp_ptr = self.Builder.gep(temp_ptr, [Constant(IntType(32), 0), index], inbounds=True)
            value = self.Builder.load(temp_ptr)
        return value

    def getType(self, type):
        if type == 'int':
            return IntType(32)
        elif type == 'char':
            return IntType(8)
        elif type == 'float':
            return FloatType()
        elif type == 'bool':
            return IntType(1)
        elif type == 'void':
            return VoidType()
        else:
            self.error("type error in <getType>")

    def getVal_local(self, id):
        temp_maps = self.var_stack[::-1]
        for map in temp_maps:
            if id in map.keys():
                return map[id]
        self.error("value error in <getVal_local>")
        return None

    def visitFunction_definition(self, ctx: SmallCParser.Function_definitionContext):
        retType = self.getType(ctx.type_specifier().getText())
        argsType = []
        argsName = []
        # args
        if ctx.param_decl_list():
            args = ctx.param_decl_list()

            for t in args.getChildren():
                if t.getText() != ',':
                    argsType.append(self.getType(t.type_specifier().getText()))
                    argsName.append(t.identifier().getText())
            funcType = FunctionType(retType, tuple(argsType))
        # no args
        else:
            funcType = FunctionType(retType, ())

        # function
        if ctx.identifier().getText() in self.function_dict:
            func = self.function_dict[ctx.identifier().getText()]
        else:
            func = Function(self.Module, funcType, name=ctx.identifier().getText())
            self.function_dict[ctx.identifier().getText()] = func
        # blocks or ;
        if ctx.compound_stmt():
            self.function = ctx.identifier().getText()
            block = func.append_basic_block(ctx.identifier().getText())
            varDict = dict()
            self.Builder = IRBuilder(block)
            for i, arg in enumerate(func.args):
                arg.name = argsName[i]
                alloca = self.Builder.alloca(arg.type, name=arg.name)
                self.Builder.store(arg, alloca)
                varDict[arg.name] = alloca
            self.var_stack.append(varDict)
            self.visit(ctx.compound_stmt())
            if isinstance(retType, VoidType):
                self.Builder.ret_void()
            self.var_stack.pop()
            self.function = None
        return

    def visitFunctioncall(self, ctx: SmallCParser.FunctioncallContext):
        var_map = self.var_stack[-1]
        args = []
        if ctx.param_list():
            for param in ctx.param_list().getChildren():
                if(param.getText() == ','):
                    continue
                temp = self.getVal_of_expr(param)
                args.append(temp)
        function = self.function_dict[ctx.identifier().getText()]
        return self.Builder.call(function, args)

    # def visitVar_decl(self, ctx: SmallCParser.Var_declContext):
    #     type = self.getType(ctx.type_specifier())
    #     list = ctx.var_decl_list()
    #     for var in list.getChildren():
    #         if var.getText() != ',':
    #             if self.builder:
    #                 alloca = self.builder.alloca(type, name=var.identifier().getText())
    #                 self.builder.store(Constant(type, None), alloca)
    #                 self.var_stack[-1][var.identifier().getText()] = alloca
    #             else:
    #                 g_var = GlobalVariable(self.Module, type, var.identifier().getText())
    #                 g_var.initializer = Constant(type, None)
    #     return

    def visitStmt(self, ctx: SmallCParser.StmtContext):
        if ctx.RETURN():
            value = self.getVal_of_expr(ctx.expr())
            return self.Builder.ret(value)
        elif ctx.CONTINUE():
            loop_blocks = self.loop_stack[-1]
            self.Builder.branch(loop_blocks['continue'])
            self.Builder.position_at_start(loop_blocks['buf'])
            return None
        elif ctx.BREAK():
            loop_blocks = self.loop_stack[-1]
            self.Builder.branch(loop_blocks['break'])
            self.Builder.position_at_start(loop_blocks['buf'])
        else:
            return self.visitChildren(ctx)

    def visitCompound_stmt(self, ctx: SmallCParser.Compound_stmtContext):
        # builder = IRBuilder(self.block_stack[-1])
        # block = self.Builder.append_basic_block()
        # self.block_stack.append(block)
        # with self.Builder.goto_block(block):
        result = self.visitChildren(ctx)
        # self.block_stack.pop()
        return result

    def visitAssignment(self, ctx: SmallCParser.AssignmentContext):
        value = self.getVal_of_expr(ctx.expr())
        identifier = ctx.identifier()
        identifier = self.getVal_local(identifier.IDENTIFIER().getText())
        if isinstance(identifier['type'],ArrayType):
            index = self.getVal_of_expr(ctx.identifier().array_indexing().expr())
            tempPtr = self.Builder.gep(identifier['ptr'],[Constant(IntType(32),0),index], inbounds=True)
            return self.Builder.store(value, tempPtr)
        return self.Builder.store(value, identifier['ptr'])

    def visitExpr(self, ctx: SmallCParser.ExprContext):
        if ctx.condition():
            return self.visit(ctx.condition())
        elif ctx.assignment():
            return self.visit(ctx.assignment())
        elif ctx.functioncall():
            return self.visit(ctx.functioncall())

    def visitCondition(self, ctx:SmallCParser.ConditionContext):
        if ctx.expr():
            disjunction = self.getVal_of_expr(ctx.disjunction())
            expr = self.getVal_of_expr(ctx.expr())
            condition = self.getVal_of_expr(ctx.condition())
            return self.Builder.select(disjunction,expr,condition)
        else:
            return self.getVal_of_expr(ctx.disjunction())

    def visitDisjunction(self, ctx:SmallCParser.DisjunctionContext):
        if ctx.disjunction():
            disjunction = self.getVal_of_expr(ctx.disjunction())
            conjunction = self.getVal_of_expr(ctx.conjunction())
            left = self.Builder.icmp_signed('!=',disjunction,Constant(disjunction.type,0))
            right = self.Builder.icmp_signed('!=', conjunction, Constant(conjunction.type, 0))
            return self.Builder.or_(left,right)
        else:
            return self.getVal_of_expr(ctx.conjunction())

    def visitConjunction(self, ctx:SmallCParser.ConjunctionContext):
        if ctx.conjunction():
            conjunction = self.getVal_of_expr(ctx.conjunction())
            comparison = self.getVal_of_expr(ctx.comparison())
            left = self.Builder.icmp_signed('!=', conjunction, Constant(conjunction.type, 0))
            right = self.Builder.icmp_signed('!=', comparison, Constant(comparison.type, 0))
            return self.Builder.and_(left,right)
        else:
            return self.getVal_of_expr(ctx.comparison())

    def visitComparison(self, ctx:SmallCParser.ComparisonContext):
        if ctx.EQUALITY():
            relation1 = self.getVal_of_expr(ctx.relation(0))
            relation2 = self.getVal_of_expr(ctx.relation(1))
            return self.Builder.icmp_signed('==',relation1,relation2)
        elif ctx.NEQUALITY():
            relation1 = self.getVal_of_expr(ctx.relation(0))
            relation2 = self.getVal_of_expr(ctx.relation(1))
            return self.Builder.icmp_signed('!=', relation1, relation2)
        else:
            return self.getVal_of_expr(ctx.relation(0))

    def visitRelation(self, ctx:SmallCParser.RelationContext):
        if len(ctx.equation()) > 1:
            equation1 = self.getVal_of_expr(ctx.equation(0))
            equation2 = self.getVal_of_expr(ctx.equation(1))
            if ctx.LEFTANGLE():
                value = self.Builder.icmp_signed('<',equation1,equation2)
            elif ctx.RIGHTANGLE():
                value = self.Builder.icmp_signed('>',equation1,equation2)
            elif ctx.LEFTANGLEEQUAL():
                value = self.Builder.icmp_signed('<=',equation1,equation2)
            elif ctx.RIGHTANGLEEQUAL():
                value = self.Builder.icmp_signed('>=',equation1,equation2)
            return value
        else:
            return self.getVal_of_expr(ctx.equation(0))

    def visitFor_stmt(self, ctx: SmallCParser.For_stmtContext):
        func = self.function_dict[self.function]

        end_block = func.append_basic_block()
        self.var_stack.append({})
        decl_block = func.append_basic_block()
        self.var_stack.append({})
        cond_block = func.append_basic_block()
        self.var_stack.append({})
        stmt_block = func.append_basic_block()
        self.var_stack.append({})
        loop_block = func.append_basic_block()

        self.loop_stack.append({'continue': cond_block, 'break': end_block, 'buf': loop_block})

        with self.Builder.goto_block(decl_block):
        # self.Builder.position_at_start(end_block)
            if ctx.var_decl():
                self.visit(ctx.var_decl())
            elif ctx.var_decl_list():
                self.visit(ctx.var_decl_list())
            else:
                self.error("for error in <visitFor_stmt>")
            self.Builder.branch(cond_block)

        self.Builder.branch(decl_block)
        with self.Builder.goto_block(cond_block):
            # cond_expr
            cond_expr = ctx.expr(0)
            cond_expr = self.visit(cond_expr)
            cond_expr = self.toBool(cond_expr)
            self.Builder.cbranch(cond_expr, stmt_block, end_block)

        with self.Builder.goto_block(stmt_block):
            # expr
            expr = ctx.expr(1)
            self.visit(expr)
            self.visit(ctx.stmt())
            self.Builder.branch(cond_block)

        self.Builder.position_at_start(end_block)

        self.loop_stack.pop()

        self.var_stack.pop()
        self.var_stack.pop()
        self.var_stack.pop()
        self.var_stack.pop()

    def visitWhile_stmt(self, ctx: SmallCParser.While_stmtContext):
        func = self.function_dict[self.function]

        end_block = func.append_basic_block()
        self.var_stack.append({})
        cond_block = func.append_basic_block()
        self.var_stack.append({})
        stmt_block = func.append_basic_block()
        self.var_stack.append({})
        loop_block = func.append_basic_block()

        self.loop_stack.append({'continue': cond_block, 'break': end_block, 'buf': loop_block})

        self.Builder.branch(cond_block)

        with self.Builder.goto_block(cond_block):
            expr = self.getVal_of_expr(ctx.expr())
            cond_expr = self.toBool(expr)
            self.Builder.cbranch(cond_expr, stmt_block, end_block)

        with self.Builder.goto_block(stmt_block):
            self.visit(ctx.stmt())
            self.Builder.branch(cond_block)

        self.Builder.position_at_start(end_block)

        self.loop_stack.pop()

        self.var_stack.pop()
        self.var_stack.pop()
        self.var_stack.pop()

    def visitCond_stmt(self, ctx: SmallCParser.Cond_stmtContext):
        var_map = self.var_stack[-1]

        expr = self.getVal_of_expr(ctx.expr())

        cond_expr = self.toBool(expr)
        else_expr = ctx.ELSE()

        if else_expr:
            with self.Builder.if_else(cond_expr) as (then, otherwise):
                with then:
                    true_stmt = ctx.stmt(0)
                    self.visit(true_stmt)
                with otherwise:
                    else_stmt = ctx.stmt(1)
                    self.visit(else_stmt)
        else:
            with self.Builder.if_then(cond_expr):
                true_stmt = ctx.stmt(0)
                self.visit(true_stmt)

    def visitVar_decl(self, ctx: SmallCParser.Var_declContext):
        self.cur_decl_type = self.getType(ctx.type_specifier().getText())
        return self.visitChildren(ctx)

    def visitVar_decl_list(self, ctx: SmallCParser.Var_decl_listContext):
        ans = []
        decls = ctx.variable_id()
        for decl in decls:
            ans.append(self.visit(decl))
        return ans

    def visitVariable_id(self, ctx: SmallCParser.Variable_idContext):
        identifier = ctx.identifier()
        var_map = self.var_stack[-1]
        type = self.cur_decl_type
        if identifier.array_indexing():
            length = self.getVal_of_expr(identifier.array_indexing().expr())
            type = ArrayType(type,length.constant)
            ptr = self.Builder.alloca(typ=type, name=identifier.IDENTIFIER().getText())
        else:
            ptr = self.Builder.alloca(typ=type, name=identifier.IDENTIFIER().getText())

        expr = ctx.expr()
        if expr:
            value = self.getVal_of_expr(expr)
        else:
            value = Constant(type, None)
        self.Builder.store(value, ptr)
        var_map[identifier.IDENTIFIER().getText()] = {"id": identifier.IDENTIFIER().getText(), "type": type, "value": value, "ptr": ptr}
        return ptr

    def visitPrimary(self, ctx: SmallCParser.PrimaryContext):
        if ctx.BOOLEAN():
            return Constant(IntType(1), ctx.getText())
        elif ctx.INTEGER():
            return Constant(IntType(32), int(ctx.getText()))
        elif ctx.REAL():
            return Constant(FloatType, ctx.getText())
        elif ctx.CHARCONST():
            return Constant(IntType(8), ctx.getText())
        elif ctx.identifier():
            return ctx.identifier()
        elif ctx.functioncall():
            return self.visit(ctx.functioncall())
        elif ctx.expr():
            return self.visit(ctx.expr())
        else:
            return self.error("type error in <visitPrimary>")


    def visitFactor(self, ctx: SmallCParser.FactorContext):
        return self.visitChildren(ctx)

    def visitTerm(self, ctx:SmallCParser.TermContext):
        if(ctx.ASTERIKS()):
            return self.Builder.mul(self.getVal_of_expr(ctx.term()), self.getVal_of_expr(ctx.factor()))
        if(ctx.SLASH()):
            return self.Builder.fdiv(self.getVal_of_expr(ctx.term()), self.getVal_of_expr(ctx.factor()))
        return self.visitChildren(ctx)

    def visitEquation(self, ctx:SmallCParser.EquationContext):
        if(ctx.PLUS()):
            return self.Builder.add(self.getVal_of_expr(ctx.equation()),self.getVal_of_expr(ctx.term()))
        if(ctx.MINUS()):
            return self.Builder.sub(self.getVal_of_expr(ctx.equation()), self.getVal_of_expr(ctx.term()))
        return self.visitChildren(ctx)