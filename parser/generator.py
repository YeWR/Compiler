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
        self.block_stack = []
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

    def toBool(self, builder, value):
        zero = Constant(self.getType('bool'), 0)
        return builder.icmp_signed('!=', value, zero)

    def getVal_of_expr(self, expr):
        var_map = self.var_stack[-1]
        temp = self.visit(expr)
        if not isinstance(temp, Constant):
            temp_ptr = var_map[temp.getText()]['ptr']
            value = self.Builder.load(temp_ptr)
        else:
            value = temp
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
        else:
            self.error("type error in <getType>")

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
            self.block_stack.append(block)
            self.var_stack.append(varDict)
            self.visit(ctx.compound_stmt())
            self.block_stack.pop()
            self.var_stack.pop()
            self.function = None
        return

    def visitFunctioncall(self, ctx: SmallCParser.FunctioncallContext):
        args = []
        if ctx.param_list():
            for param in ctx.param_list().getChildren():
                temp = self.visit(param)
                args.append(temp)
        return self.Builder.call(self.function_dict[ctx.identifier().getText()], args)

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
            self.Builder.ret(Constant(self.getType('int'), value))
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
        return self.visitChildren(ctx)
        # block = self.Builder.block
        # identifier = ctx.identifier()
        # expr = self.visit(ctx.expr())
        # result = self.Builder().store(value=expr, ptr=, align=4)

    # def visitExpr(self, ctx: SmallCParser.ExprContext):
    #     if ctx.condition():
    #         return self.visit(ctx.condition())
    #     elif ctx.assignment():
    #         return self.visit(ctx.assignment())
    #     elif ctx.functioncall():
    #         return self.visit(ctx.functioncall())
    #
    # def visitCondition(self, ctx:SmallCParser.ConditionContext):
    #     if ctx.expr():
    #         disjunction = self.visit(ctx.disjunction())
    #         expr = self.visit(ctx.expr())
    #         condition = self.visit(ctx.condition())
    #     else:
    #         return self.visit(ctx.disjunction())
    #
    # def visitDisjunction(self, ctx:SmallCParser.DisjunctionContext):
    #     if ctx.disjunction():
    #         disjunction = self.visit(ctx.disjunction())
    #         conjunction = self.visit(ctx.conjunction())
    #     else:
    #         return self.visit(ctx.conjunction())
    #
    # def visitConjunction(self, ctx:SmallCParser.ConjunctionContext):
    #     if ctx.conjunction():
    #         conjunction = self.visit(ctx.conjunction())
    #         comparison = self.visit(ctx.comparison())
    #     else:
    #         return self.visit(ctx.comparison())
    #
    # def visitComparison(self, ctx:SmallCParser.ComparisonContext):
    #     if ctx.EQUALITY():
    #         relation1 = self.visit(ctx.relation(0))
    #         relation2 = self.visit(ctx.relation(1))
    #     elif ctx.NEQUALITY():
    #         relation1 = self.visit(ctx.relation(0))
    #         relation2 = self.visit(ctx.relation(1))
    #     else:
    #         return self.visit(ctx.relation())

    # def visitRelation(self, ctx:SmallCParser.RelationContext):

    def visitCond_stmt(self, ctx: SmallCParser.Cond_stmtContext):
        var_map = self.var_stack[-1]

        expr = self.getVal_of_expr(ctx.expr())

        cond_expr = self.toBool(self.Builder, expr)
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
        ptr = self.Builder.alloca(typ=type, name=identifier.getText())

        expr = ctx.expr()
        if expr:
            value = self.getVal_of_expr(expr)
        else:
            value = Constant(type, None)

        self.Builder.store(value, ptr)

        var_map[identifier.getText()] = {"id": identifier.getText(), "type": type, "value": value, "ptr": ptr}
        return ptr

    def visitExpr(self, ctx: SmallCParser.ExprContext):
        return self.visitChildren(ctx)

    def visitPrimary(self, ctx: SmallCParser.PrimaryContext):
        if ctx.BOOLEAN():
            return Constant(IntType(1), ctx.getText())
        elif ctx.INTEGER():
            return Constant(IntType(32), ctx.getText())
        elif ctx.REAL():
            return Constant(FloatType, ctx.getText())
        elif ctx.CHARCONST():
            return Constant(IntType(8), ctx.getText())
        elif ctx.identifier():
            return ctx.identifier()
        elif ctx.functioncall():
            return self.visitChildren(ctx)
        elif ctx.expr():
            return ctx.expr()
        else:
            return self.error("type error in <visitPrimary>")
