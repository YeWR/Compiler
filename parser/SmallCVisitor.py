# Generated from SmallC.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SmallCParser import SmallCParser
else:
    from SmallCParser import SmallCParser

# This class defines a complete generic visitor for a parse tree produced by SmallCParser.

class SmallCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SmallCParser#smallc_program.
    def visitSmallc_program(self, ctx:SmallCParser.Smallc_programContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#function_definition.
    def visitFunction_definition(self, ctx:SmallCParser.Function_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#identifier.
    def visitIdentifier(self, ctx:SmallCParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#array_indexing.
    def visitArray_indexing(self, ctx:SmallCParser.Array_indexingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#array_init.
    def visitArray_init(self, ctx:SmallCParser.Array_initContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#include.
    def visitInclude(self, ctx:SmallCParser.IncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#type_specifier.
    def visitType_specifier(self, ctx:SmallCParser.Type_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#param_decl_list.
    def visitParam_decl_list(self, ctx:SmallCParser.Param_decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#parameter_decl.
    def visitParameter_decl(self, ctx:SmallCParser.Parameter_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#param_list.
    def visitParam_list(self, ctx:SmallCParser.Param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#compound_stmt.
    def visitCompound_stmt(self, ctx:SmallCParser.Compound_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#var_decl.
    def visitVar_decl(self, ctx:SmallCParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#var_decl_list.
    def visitVar_decl_list(self, ctx:SmallCParser.Var_decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#variable_id.
    def visitVariable_id(self, ctx:SmallCParser.Variable_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#stmt.
    def visitStmt(self, ctx:SmallCParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#cond_stmt.
    def visitCond_stmt(self, ctx:SmallCParser.Cond_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#while_stmt.
    def visitWhile_stmt(self, ctx:SmallCParser.While_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#for_stmt.
    def visitFor_stmt(self, ctx:SmallCParser.For_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#expr.
    def visitExpr(self, ctx:SmallCParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#assignment.
    def visitAssignment(self, ctx:SmallCParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#functioncall.
    def visitFunctioncall(self, ctx:SmallCParser.FunctioncallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#condition.
    def visitCondition(self, ctx:SmallCParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#disjunction.
    def visitDisjunction(self, ctx:SmallCParser.DisjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#conjunction.
    def visitConjunction(self, ctx:SmallCParser.ConjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#comparison.
    def visitComparison(self, ctx:SmallCParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#relation.
    def visitRelation(self, ctx:SmallCParser.RelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#equation.
    def visitEquation(self, ctx:SmallCParser.EquationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#term.
    def visitTerm(self, ctx:SmallCParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#factor.
    def visitFactor(self, ctx:SmallCParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmallCParser#primary.
    def visitPrimary(self, ctx:SmallCParser.PrimaryContext):
        return self.visitChildren(ctx)



del SmallCParser