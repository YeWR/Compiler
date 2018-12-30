# Generated from SmallC.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SmallCParser import SmallCParser
else:
    from SmallCParser import SmallCParser

# This class defines a complete listener for a parse tree produced by SmallCParser.
class SmallCListener(ParseTreeListener):

    # Enter a parse tree produced by SmallCParser#smallc_program.
    def enterSmallc_program(self, ctx:SmallCParser.Smallc_programContext):
        pass

    # Exit a parse tree produced by SmallCParser#smallc_program.
    def exitSmallc_program(self, ctx:SmallCParser.Smallc_programContext):
        pass


    # Enter a parse tree produced by SmallCParser#function_definition.
    def enterFunction_definition(self, ctx:SmallCParser.Function_definitionContext):
        pass

    # Exit a parse tree produced by SmallCParser#function_definition.
    def exitFunction_definition(self, ctx:SmallCParser.Function_definitionContext):
        pass


    # Enter a parse tree produced by SmallCParser#identifier.
    def enterIdentifier(self, ctx:SmallCParser.IdentifierContext):
        pass

    # Exit a parse tree produced by SmallCParser#identifier.
    def exitIdentifier(self, ctx:SmallCParser.IdentifierContext):
        pass


    # Enter a parse tree produced by SmallCParser#array_indexing.
    def enterArray_indexing(self, ctx:SmallCParser.Array_indexingContext):
        pass

    # Exit a parse tree produced by SmallCParser#array_indexing.
    def exitArray_indexing(self, ctx:SmallCParser.Array_indexingContext):
        pass


    # Enter a parse tree produced by SmallCParser#array_init.
    def enterArray_init(self, ctx:SmallCParser.Array_initContext):
        pass

    # Exit a parse tree produced by SmallCParser#array_init.
    def exitArray_init(self, ctx:SmallCParser.Array_initContext):
        pass


    # Enter a parse tree produced by SmallCParser#include.
    def enterInclude(self, ctx:SmallCParser.IncludeContext):
        pass

    # Exit a parse tree produced by SmallCParser#include.
    def exitInclude(self, ctx:SmallCParser.IncludeContext):
        pass


    # Enter a parse tree produced by SmallCParser#type_specifier.
    def enterType_specifier(self, ctx:SmallCParser.Type_specifierContext):
        pass

    # Exit a parse tree produced by SmallCParser#type_specifier.
    def exitType_specifier(self, ctx:SmallCParser.Type_specifierContext):
        pass


    # Enter a parse tree produced by SmallCParser#param_decl_list.
    def enterParam_decl_list(self, ctx:SmallCParser.Param_decl_listContext):
        pass

    # Exit a parse tree produced by SmallCParser#param_decl_list.
    def exitParam_decl_list(self, ctx:SmallCParser.Param_decl_listContext):
        pass


    # Enter a parse tree produced by SmallCParser#parameter_decl.
    def enterParameter_decl(self, ctx:SmallCParser.Parameter_declContext):
        pass

    # Exit a parse tree produced by SmallCParser#parameter_decl.
    def exitParameter_decl(self, ctx:SmallCParser.Parameter_declContext):
        pass


    # Enter a parse tree produced by SmallCParser#param_list.
    def enterParam_list(self, ctx:SmallCParser.Param_listContext):
        pass

    # Exit a parse tree produced by SmallCParser#param_list.
    def exitParam_list(self, ctx:SmallCParser.Param_listContext):
        pass


    # Enter a parse tree produced by SmallCParser#compound_stmt.
    def enterCompound_stmt(self, ctx:SmallCParser.Compound_stmtContext):
        pass

    # Exit a parse tree produced by SmallCParser#compound_stmt.
    def exitCompound_stmt(self, ctx:SmallCParser.Compound_stmtContext):
        pass


    # Enter a parse tree produced by SmallCParser#var_decl.
    def enterVar_decl(self, ctx:SmallCParser.Var_declContext):
        pass

    # Exit a parse tree produced by SmallCParser#var_decl.
    def exitVar_decl(self, ctx:SmallCParser.Var_declContext):
        pass


    # Enter a parse tree produced by SmallCParser#var_decl_list.
    def enterVar_decl_list(self, ctx:SmallCParser.Var_decl_listContext):
        pass

    # Exit a parse tree produced by SmallCParser#var_decl_list.
    def exitVar_decl_list(self, ctx:SmallCParser.Var_decl_listContext):
        pass


    # Enter a parse tree produced by SmallCParser#variable_id.
    def enterVariable_id(self, ctx:SmallCParser.Variable_idContext):
        pass

    # Exit a parse tree produced by SmallCParser#variable_id.
    def exitVariable_id(self, ctx:SmallCParser.Variable_idContext):
        pass


    # Enter a parse tree produced by SmallCParser#stmt.
    def enterStmt(self, ctx:SmallCParser.StmtContext):
        pass

    # Exit a parse tree produced by SmallCParser#stmt.
    def exitStmt(self, ctx:SmallCParser.StmtContext):
        pass


    # Enter a parse tree produced by SmallCParser#cond_stmt.
    def enterCond_stmt(self, ctx:SmallCParser.Cond_stmtContext):
        pass

    # Exit a parse tree produced by SmallCParser#cond_stmt.
    def exitCond_stmt(self, ctx:SmallCParser.Cond_stmtContext):
        pass


    # Enter a parse tree produced by SmallCParser#while_stmt.
    def enterWhile_stmt(self, ctx:SmallCParser.While_stmtContext):
        pass

    # Exit a parse tree produced by SmallCParser#while_stmt.
    def exitWhile_stmt(self, ctx:SmallCParser.While_stmtContext):
        pass


    # Enter a parse tree produced by SmallCParser#for_stmt.
    def enterFor_stmt(self, ctx:SmallCParser.For_stmtContext):
        pass

    # Exit a parse tree produced by SmallCParser#for_stmt.
    def exitFor_stmt(self, ctx:SmallCParser.For_stmtContext):
        pass


    # Enter a parse tree produced by SmallCParser#expr.
    def enterExpr(self, ctx:SmallCParser.ExprContext):
        pass

    # Exit a parse tree produced by SmallCParser#expr.
    def exitExpr(self, ctx:SmallCParser.ExprContext):
        pass


    # Enter a parse tree produced by SmallCParser#assignment.
    def enterAssignment(self, ctx:SmallCParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SmallCParser#assignment.
    def exitAssignment(self, ctx:SmallCParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SmallCParser#functioncall.
    def enterFunctioncall(self, ctx:SmallCParser.FunctioncallContext):
        pass

    # Exit a parse tree produced by SmallCParser#functioncall.
    def exitFunctioncall(self, ctx:SmallCParser.FunctioncallContext):
        pass


    # Enter a parse tree produced by SmallCParser#condition.
    def enterCondition(self, ctx:SmallCParser.ConditionContext):
        pass

    # Exit a parse tree produced by SmallCParser#condition.
    def exitCondition(self, ctx:SmallCParser.ConditionContext):
        pass


    # Enter a parse tree produced by SmallCParser#disjunction.
    def enterDisjunction(self, ctx:SmallCParser.DisjunctionContext):
        pass

    # Exit a parse tree produced by SmallCParser#disjunction.
    def exitDisjunction(self, ctx:SmallCParser.DisjunctionContext):
        pass


    # Enter a parse tree produced by SmallCParser#conjunction.
    def enterConjunction(self, ctx:SmallCParser.ConjunctionContext):
        pass

    # Exit a parse tree produced by SmallCParser#conjunction.
    def exitConjunction(self, ctx:SmallCParser.ConjunctionContext):
        pass


    # Enter a parse tree produced by SmallCParser#comparison.
    def enterComparison(self, ctx:SmallCParser.ComparisonContext):
        pass

    # Exit a parse tree produced by SmallCParser#comparison.
    def exitComparison(self, ctx:SmallCParser.ComparisonContext):
        pass


    # Enter a parse tree produced by SmallCParser#relation.
    def enterRelation(self, ctx:SmallCParser.RelationContext):
        pass

    # Exit a parse tree produced by SmallCParser#relation.
    def exitRelation(self, ctx:SmallCParser.RelationContext):
        pass


    # Enter a parse tree produced by SmallCParser#equation.
    def enterEquation(self, ctx:SmallCParser.EquationContext):
        pass

    # Exit a parse tree produced by SmallCParser#equation.
    def exitEquation(self, ctx:SmallCParser.EquationContext):
        pass


    # Enter a parse tree produced by SmallCParser#term.
    def enterTerm(self, ctx:SmallCParser.TermContext):
        pass

    # Exit a parse tree produced by SmallCParser#term.
    def exitTerm(self, ctx:SmallCParser.TermContext):
        pass


    # Enter a parse tree produced by SmallCParser#factor.
    def enterFactor(self, ctx:SmallCParser.FactorContext):
        pass

    # Exit a parse tree produced by SmallCParser#factor.
    def exitFactor(self, ctx:SmallCParser.FactorContext):
        pass


    # Enter a parse tree produced by SmallCParser#primary.
    def enterPrimary(self, ctx:SmallCParser.PrimaryContext):
        pass

    # Exit a parse tree produced by SmallCParser#primary.
    def exitPrimary(self, ctx:SmallCParser.PrimaryContext):
        pass


