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
        self.signal_stack = []
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
        temp = self.visit(expr)
        if isinstance(temp, Constant) or isinstance(temp, CallInstr) or isinstance(temp, LoadInstr) or isinstance(temp,
                                                                                                                  Instruction):
            value = temp
        else:
            temp_val = self.getVal_local(temp.IDENTIFIER().getText())
            temp_ptr = temp_val['ptr']
            if temp.array_indexing():
                index = self.getVal_of_expr(temp.array_indexing().expr())
                temp_ptr = self.Builder.gep(temp_ptr, [Constant(IntType(32), 0), index], inbounds=True)
            # if isinstance(temp_val['type'],ArrayType):
            #     if temp.array_indexing():
            #         index = self.getVal_of_expr(temp.array_indexing().expr())
            #         temp_ptr = self.Builder.gep(temp_ptr, [Constant(IntType(32), 0), index], inbounds=True)
            #     elif temp.AMPERSAND():
            #         Constant(PointerType(IntType(8)), temp_ptr.getText())
            #     elif temp.ASTERIKS():
            #         pass
            #     else: #返回数组地址
            #         temp_ptr = self.Builder.gep(temp_ptr, [Constant(IntType(32), 0), Constant(IntType(32), 0)], inbounds=True)
            #         return temp_ptr
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
        if ctx.identifier().ASTERIKS():
            retType = retType.as_pointer()
        argsType = []
        argsName = []
        # args
        if ctx.param_decl_list():
            args = ctx.param_decl_list()
            var_arg = False
            for t in args.getChildren():
                if t.getText() != ',':
                    if t.getText() == '...':
                        var_arg = True
                        break
                    t_type = self.getType(t.type_specifier().getText())
                    if t.identifier().ASTERIKS():
                        t_type = t_type.as_pointer()
                    argsType.append(t_type)
                    argsName.append(t.identifier().IDENTIFIER().getText())
            funcType = FunctionType(retType, tuple(argsType), var_arg=var_arg)
        # no args
        else:
            funcType = FunctionType(retType, ())

        # function
        if ctx.identifier().IDENTIFIER().getText() in self.function_dict:
            func = self.function_dict[ctx.identifier().IDENTIFIER().getText()]
        else:
            func = Function(self.Module, funcType, name=ctx.identifier().IDENTIFIER().getText())
            self.function_dict[ctx.identifier().IDENTIFIER().getText()] = func
        # blocks or ;
        if ctx.compound_stmt():
            self.function = ctx.identifier().IDENTIFIER().getText()
            block = func.append_basic_block(ctx.identifier().IDENTIFIER().getText())
            varDict = dict()
            self.Builder = IRBuilder(block)
            for i, arg in enumerate(func.args):
                arg.name = argsName[i]
                alloca = self.Builder.alloca(arg.type, name=arg.name)
                self.Builder.store(arg, alloca)
                varDict[arg.name] = {"id": arg.name, "type": arg.type, "value": None, "ptr": alloca}
            self.var_stack.append(varDict)
            self.visit(ctx.compound_stmt())
            if isinstance(retType, VoidType):
                self.Builder.ret_void()
            self.var_stack.pop()
            self.function = None
        return

    def visitFunctioncall(self, ctx: SmallCParser.FunctioncallContext):
        var_map = self.var_stack[-1]
        function = self.function_dict[ctx.identifier().getText()]
        arg_types = function.args
        index = 0

        args = []
        if ctx.param_list():
            for param in ctx.param_list().getChildren():
                if (param.getText() == ','):
                    continue

                temp = self.getVal_of_expr(param)

                arg_type = None
                if index < len(arg_types):
                    arg_type = arg_types[index]
                ptr_flag = False
                if arg_type:
                    if isinstance(arg_type.type, PointerType):
                        ptr_flag = True
                else:
                    temp_type = var_map[temp.name]['type']
                    if isinstance(temp_type, PointerType):
                        ptr_flag = True
                if not ptr_flag:
                    temp = self.Builder.load(temp)
                args.append(temp)

                index += 1

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
            self.signal_stack[-1] = 1
            loop_blocks = self.loop_stack[-1]
            self.Builder.branch(loop_blocks['continue'])
            self.Builder.position_at_start(loop_blocks['buf'])
            return None
        elif ctx.BREAK():
            self.signal_stack[-1] = -1
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
        if isinstance(identifier['type'], ArrayType):
            if ctx.identifier().array_indexing():
                index = self.getVal_of_expr(ctx.identifier().array_indexing().expr())
                if isinstance(index.type, PointerType):
                    index = self.Builder.load(index)
            else:
                index = Constant(IntType(32), 0)
            tempPtr = self.Builder.gep(identifier['ptr'], [Constant(IntType(32), 0), index], inbounds=True)
            if isinstance(value, GEPInstr):
                value = self.Builder.load(value)
            return self.Builder.store(value, tempPtr)
        if isinstance(value.type, PointerType):
            value = self.Builder.load(value)
        return self.Builder.store(value, identifier['ptr'])

    def visitExpr(self, ctx: SmallCParser.ExprContext):
        if ctx.condition():
            return self.visit(ctx.condition())
        elif ctx.assignment():
            return self.visit(ctx.assignment())
        elif ctx.functioncall():
            return self.visit(ctx.functioncall())

    def visitCondition(self, ctx: SmallCParser.ConditionContext):
        if ctx.expr():
            disjunction = self.getVal_of_expr(ctx.disjunction())
            if isinstance(disjunction.type, PointerType):
                disjunction = self.Builder.load(disjunction)
            cond = self.Builder.icmp_signed('!=', disjunction, Constant(disjunction.type, 0))
            expr = self.getVal_of_expr(ctx.expr())
            if isinstance(expr.type, PointerType):
                expr = self.Builder.load(expr)
            condition = self.getVal_of_expr(ctx.condition())
            return self.Builder.select(cond, expr, condition)
        else:
            return self.getVal_of_expr(ctx.disjunction())

    def visitDisjunction(self, ctx: SmallCParser.DisjunctionContext):
        if ctx.disjunction():
            disjunction = self.getVal_of_expr(ctx.disjunction())
            if isinstance(disjunction.type, PointerType):
                disjunction = self.Builder.load(disjunction)
            conjunction = self.getVal_of_expr(ctx.conjunction())
            if isinstance(conjunction.type, PointerType):
                conjunction = self.Builder.load(conjunction)
            left = self.Builder.icmp_signed('!=', disjunction, Constant(disjunction.type, 0))
            right = self.Builder.icmp_signed('!=', conjunction, Constant(conjunction.type, 0))
            return self.Builder.or_(left, right)
        else:
            return self.getVal_of_expr(ctx.conjunction())

    def visitConjunction(self, ctx: SmallCParser.ConjunctionContext):
        if ctx.conjunction():
            conjunction = self.getVal_of_expr(ctx.conjunction())
            if isinstance(conjunction.type, PointerType):
                conjunction = self.Builder.load(conjunction)
            comparison = self.getVal_of_expr(ctx.comparison())
            if isinstance(comparison.type, PointerType):
                comparison = self.Builder.load(comparison)
            left = self.Builder.icmp_signed('!=', conjunction, Constant(conjunction.type, 0))
            right = self.Builder.icmp_signed('!=', comparison, Constant(comparison.type, 0))
            return self.Builder.and_(left, right)
        else:
            return self.getVal_of_expr(ctx.comparison())

    def visitComparison(self, ctx: SmallCParser.ComparisonContext):
        if ctx.EQUALITY():
            relation1 = self.getVal_of_expr(ctx.relation(0))
            if isinstance(relation1.type, PointerType):
                relation1 = self.Builder.load(relation1)
            relation2 = self.getVal_of_expr(ctx.relation(1))
            if isinstance(relation2.type, PointerType):
                relation2 = self.Builder.load(relation2)
            return self.Builder.icmp_signed('==', relation1, relation2)
        elif ctx.NEQUALITY():
            relation1 = self.getVal_of_expr(ctx.relation(0))
            if isinstance(relation1.type, PointerType):
                relation1 = self.Builder.load(relation1)
            relation2 = self.getVal_of_expr(ctx.relation(1))
            if isinstance(relation2.type, PointerType):
                relation2 = self.Builder.load(relation2)
            return self.Builder.icmp_signed('!=', relation1, relation2)
        else:
            return self.getVal_of_expr(ctx.relation(0))

    def visitRelation(self, ctx: SmallCParser.RelationContext):
        if len(ctx.equation()) > 1:
            equation1 = self.getVal_of_expr(ctx.equation(0))
            if isinstance(equation1.type, PointerType):
                equation1 = self.Builder.load(equation1)
            equation2 = self.getVal_of_expr(ctx.equation(1))
            if isinstance(equation2.type, PointerType):
                equation2 = self.Builder.load(equation2)
            if ctx.LEFTANGLE():
                value = self.Builder.icmp_signed('<', equation1, equation2)
            elif ctx.RIGHTANGLE():
                value = self.Builder.icmp_signed('>', equation1, equation2)
            elif ctx.LEFTANGLEEQUAL():
                value = self.Builder.icmp_signed('<=', equation1, equation2)
            elif ctx.RIGHTANGLEEQUAL():
                value = self.Builder.icmp_signed('>=', equation1, equation2)
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
        # 1 -> continue, -1 -> break
        self.signal_stack.append(0)

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
            if self.signal_stack[-1] == 0:
                loop_blocks = self.loop_stack[-1]
                self.Builder.position_at_start(loop_blocks['buf'])
                self.Builder.branch(end_block)

        self.Builder.position_at_start(end_block)

        self.loop_stack.pop()
        self.signal_stack.pop()

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
        # 1 -> continue, -1 -> break
        self.signal_stack.append(0)

        self.loop_stack.append({'continue': cond_block, 'break': end_block, 'buf': loop_block})

        self.Builder.branch(cond_block)

        with self.Builder.goto_block(cond_block):
            expr = self.getVal_of_expr(ctx.expr())
            cond_expr = self.toBool(expr)
            self.Builder.cbranch(cond_expr, stmt_block, end_block)

        with self.Builder.goto_block(stmt_block):
            self.visit(ctx.stmt())
            self.Builder.branch(cond_block)
            if self.signal_stack[-1] == 0:
                loop_blocks = self.loop_stack[-1]
                self.Builder.position_at_start(loop_blocks['buf'])
                self.Builder.branch(end_block)

        self.Builder.position_at_start(end_block)

        self.loop_stack.pop()
        self.signal_stack.pop()

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
        type = self.cur_decl_type

        if not self.function:
            if identifier.array_indexing():
                length = self.getVal_of_expr(identifier.array_indexing().expr())
                type = ArrayType(type, length.constant)
                g_var = GlobalVariable(self.Module, type, identifier.IDENTIFIER().getText())
            else:
                g_var = GlobalVariable(self.Module, type, identifier.IDENTIFIER().getText())

            g_var.initializer = Constant(type, None)
            atomic = {"id": identifier.IDENTIFIER().getText(), "type": type,
                                                      "value": None, "ptr": g_var}
            if not len(self.var_stack):
                self.var_stack.append({})
            self.var_stack[0][identifier.IDENTIFIER().getText()] = atomic
            return g_var

        var_map = self.var_stack[-1]

        if identifier.array_indexing():
            length = self.getVal_of_expr(identifier.array_indexing().expr())
            type = ArrayType(type, length.constant)
            ptr = self.Builder.alloca(typ=type, name=identifier.IDENTIFIER().getText())
        else:
            ptr = self.Builder.alloca(typ=type, name=identifier.IDENTIFIER().getText())

        expr = ctx.expr()
        if expr:
            value = self.getVal_of_expr(expr)
        else:
            value = Constant(type, None)
        self.Builder.store(value, ptr)
        var_map[identifier.IDENTIFIER().getText()] = {"id": identifier.IDENTIFIER().getText(), "type": type,
                                                      "value": value, "ptr": ptr}
        return ptr

    def visitPrimary(self, ctx: SmallCParser.PrimaryContext):
        if ctx.BOOLEAN():
            return Constant(IntType(1), bool(ctx.getText()))
        elif ctx.INTEGER():
            return Constant(IntType(32), int(ctx.getText()))
        elif ctx.REAL():
            return Constant(FloatType, float(ctx.getText()))
        elif ctx.CHARCONST():
            tempStr = ctx.getText()[1:-1]
            tempStr = tempStr.replace('\\n', '\n')
            tempStr = tempStr.replace('\\0', '\0')
            if ctx.getText()[0] == '"':
                tempStr += '\0'
                temp = GlobalVariable(self.Module, ArrayType(IntType(8), len(tempStr)), name="str_" + tempStr)
                temp.initializer = Constant(ArrayType(IntType(8), len(tempStr)), bytearray(tempStr, encoding='utf-8'))
                temp.global_constant = True
                return self.Builder.gep(temp, [Constant(IntType(32), 0), Constant(IntType(32), 0)], inbounds=True)
            return Constant(IntType(8), ord(tempStr[0]))
        elif ctx.identifier():
            return self.visit(ctx.identifier())
        elif ctx.functioncall():
            return self.visit(ctx.functioncall())
        elif ctx.expr():
            return self.visit(ctx.expr())
        else:
            return self.error("type error in <visitPrimary>")

    def visitFactor(self, ctx: SmallCParser.FactorContext):
        return self.visitChildren(ctx)

    def visitTerm(self, ctx: SmallCParser.TermContext):
        if (ctx.ASTERIKS()):
            term = self.getVal_of_expr(ctx.term())
            if isinstance(term.type, PointerType):
                term = self.Builder.load(term)
            factor = self.getVal_of_expr(ctx.factor())
            if isinstance(factor.type, PointerType):
                factor = self.Builder.load(factor)
            return self.Builder.mul(term, factor)
        if (ctx.SLASH()):
            term = self.getVal_of_expr(ctx.term())
            if isinstance(term.type, PointerType):
                term = self.Builder.load(term)
            factor = self.getVal_of_expr(ctx.factor())
            if isinstance(factor.type, PointerType):
                factor = self.Builder.load(factor)
            return self.Builder.fdiv(term, factor)
        return self.visitChildren(ctx)

    def visitEquation(self, ctx: SmallCParser.EquationContext):
        if (ctx.PLUS()):
            equation = self.getVal_of_expr(ctx.equation())
            if isinstance(equation.type, PointerType):
                equation = self.Builder.load(equation)
            term = self.getVal_of_expr(ctx.term())
            if isinstance(term.type, PointerType):
                term = self.Builder.load(term)
            return self.Builder.add(equation, term)
        if (ctx.MINUS()):
            equation = self.getVal_of_expr(ctx.equation())
            if isinstance(equation.type, PointerType):
                equation = self.Builder.load(equation)
            term = self.getVal_of_expr(ctx.term())
            if isinstance(term.type, PointerType):
                term = self.Builder.load(term)
            return self.Builder.sub(equation, term)
        return self.visitChildren(ctx)

    def visitIdentifier(self, ctx: SmallCParser.IdentifierContext):
        if (ctx.AMPERSAND() and ctx.array_indexing()):
            return self.Builder.gep(self.getVal_of_expr(ctx.IDENTIFIER()), self.getVal_of_expr(ctx.array_indexing()))
        if (ctx.ASTERIKS() and ctx.array_indexing()):
            return self.Builder.load(
                self.Builder.gep(self.getVal_of_expr(ctx.IDENTIFIER()), self.getVal_of_expr(ctx.array_indexing())))
        if (ctx.AMPERSAND()):
            return self.getVal_local(str(ctx.IDENTIFIER()))['ptr']
        if (ctx.ASTERIKS()):
            return self.getVal_local(str(ctx.IDENTIFIER()))['ptr']
        temp = self.getVal_local(ctx.IDENTIFIER().getText())
        temp_ptr = temp['ptr']
        # if isinstance(temp_val['type'],ArrayType):
        #     if temp.array_indexing():
        #         index = self.getVal_of_expr(temp.array_indexing().expr())
        #         temp_ptr = self.Builder.gep(temp_ptr, [Constant(IntType(32), 0), index], inbounds=True)
        #     elif temp.AMPERSAND():
        #         Constant(PointerType(IntType(8)), temp_ptr.getText())
        #     elif temp.ASTERIKS():
        #         pass
        #     else: #返回数组地址
        #         temp_ptr = self.Builder.gep(temp_ptr, [Constant(IntType(32), 0), Constant(IntType(32), 0)], inbounds=True)
        #         return temp_ptr
        if isinstance(temp['type'], ArrayType):
            if ctx.array_indexing():
                index = self.getVal_of_expr(ctx.array_indexing().expr())
                if isinstance(index.type, PointerType):
                    index = self.Builder.load(index)
                temp_ptr = self.Builder.gep(temp_ptr, [Constant(IntType(32), 0), index], inbounds=True)
                return temp_ptr
            else:
                temp_ptr = self.Builder.gep(temp_ptr, [Constant(IntType(32), 0), Constant(IntType(32), 0)],
                                            inbounds=True)
                return temp_ptr
        temp_val = temp['ptr']
        return temp_val

    def visitArray_indexing(self, ctx: SmallCParser.Array_indexingContext):
        return self.visit(ctx.expr())
