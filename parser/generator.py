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
                alloca = self.Builder.alloca(arg.type,name=arg.name)
                self.Builder.store(arg,alloca)
                varDict[arg.name] = alloca
            self.block_stack.append(block)
            self.var_stack.append(varDict)
            self.visit(ctx.compound_stmt())
            self.block_stack.pop()
            self.var_stack.pop()
            self.function = None
            self.Builder = None


    def visitVar_decl(self, ctx:SmallCParser.Var_declContext):
        type = self.getType(ctx.type_specifier().getText())
        list = ctx.var_decl_list()
        for var in list.getChildren():
            if var.getText() != ';' and ',':
                if self.Builder:
                    alloca = self.Builder.alloca(type, name=var.identifier().getText())
                    self.Builder.store(Constant(type,None),alloca)
                    self.var_stack[-1][var.identifier().getText()] = alloca
                else:
                    g_var = GlobalVariable(self.Module, type, var.identifier().getText())
                    g_var.initializer = Constant(type, None)
        return

    def visitStmt(self, ctx:SmallCParser.StmtContext):
        return

    def visitCompound_stmt(self, ctx: SmallCParser.Compound_stmtContext):
        self.visitChildren(ctx)

    def visitAssignment(self, ctx: SmallCParser.AssignmentContext):
        return
        # block = self.Builder.block
        # identifier = ctx.identifier()
        # expr = self.visit(ctx.expr())
        # result = self.Builder().store(value=expr, ptr=, align=4)

    def visitExpr(self, ctx: SmallCParser.ExprContext):
        return self.visitChildren(ctx)

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
        builder = IRBuilder(self.block_stack[-1])
        ptr = builder.alloca(typ=self.cur_decl_type, name=identifier.getText())

        expr = ctx.expr()
        if expr:
            value = self.visit(expr)
        else:
            value = Constant(self.cur_decl_type, None)

        builder.store(value, ptr)

        var_map = self.var_stack[-1]
        var_map[identifier.getText()] = {"value": value, "ptr": ptr}
        return ptr

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
            return
        elif ctx.functioncall():
            return
        elif ctx.expr():
            return
        else:
            return self.error("type error in <visitPrimary>")
