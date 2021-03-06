from run_pipeline import run_pipeline
from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker
from src.tset_builder import TSetBuilder
from src.tsets_reducer import TSetReducer
from src.tset_merger import TSetMerger
from src.cool_visitor import FormatVisitor

# Probando inferencia en funciones recursivas
# Se infiere:
# a : Int porque se usa en una operacion aritmetica
# b : Int porque se usa en una operacion aritmetica
# f() : Int
# g() : Int
# Una vez inferido el tipo de a y b, en las proximas pasadas se infiere que el if devuelve Int en ambos metodos


def test():
    text = """

     class Main {
    main (): Object {
        0
    };

    f(a: AUTO_TYPE, b: AUTO_TYPE): AUTO_TYPE {
        if a = 1 then b else
            g(a + 1, b / 1)
        fi
    };

    g(a: AUTO_TYPE, b: AUTO_TYPE): AUTO_TYPE {
        if b = 1 then a else
            f(a / 2, b + 1)
        fi
    };
};
        """

    ast = run_pipeline(text)
    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    checker = TypeChecker(context, errors)
    checker.visit(ast, None)

    print(errors)
    if errors != []:
        print(errors)
        assert False

    tset_builder = TSetBuilder(context, errors)
    tset = tset_builder.visit(ast, None)

    tset_reducer = TSetReducer(context, errors)
    reduced_set = tset_reducer.visit(ast, tset)

    tset_merger = TSetMerger(context, errors)
    tset_merger.visit(ast, reduced_set)

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    checker = TypeChecker(context, errors)
    checker.visit(ast, None)

    formatter = FormatVisitor()
    tree = formatter.visit(ast)

    print("Errors:", errors)
    print("Context:")
    print(context)
    print(reduced_set)
    print(tree)

    assert errors == []
