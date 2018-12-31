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
        self.Builder = IRBuilder
        self.NamedValues = dict()
        self.counter = 0
        self.block_stack = []

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
        # args
        if ctx.param_decl_list():
            args = ctx.param_decl_list()
            argsType = []
            for t in args.getChildren():
                if t.getText() != ',':
                    argsType.append(self.getType(t.type_specifier().getText()))
            funcType = FunctionType(retType, tuple(argsType))
        # no args
        else:
            funcType = FunctionType(retType, ())

        # function
        func = Function(self.Module, funcType, name=ctx.identifier().getText())
        self.function_dict[ctx.identifier().getText()] = func

        block = func.append_basic_block(name="label_" + str(self.counter))
        self.counter += 1

        # blocks or ;
        self.visit(ctx.compound_stmt())

    def visitCompound_stmt(self, ctx: SmallCParser.Compound_stmtContext):
        self.visitChildren(ctx)

    def visitAssignment(self, ctx: SmallCParser.AssignmentContext):
        pass
        # block = self.Builder.block
        # identifier = ctx.identifier()
        # expr = self.visit(ctx.expr())
        # result = self.Builder().store(value=expr, ptr=, align=4)

    def visitExpr(self, ctx: SmallCParser.ExprContext):
        return self.visitChildren(ctx)

    def getPtr(self, identifier):
        return Constant(PointerType, identifier.getText())

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
