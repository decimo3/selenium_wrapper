import ast
from pathlib import Path
from dataclasses import dataclass
from dotenv import dotenv_values

@dataclass(frozen=True)
class LangReference:
    file: Path
    line: int
    property: str

class LangVisitor(ast.NodeVisitor):
    def __init__(self, file: Path):
        self.file = file
        self.references: list[LangReference] = []
    def visit_Attribute(self, node):
        if (
            isinstance(node.value, ast.Name)
            and node.value.id == "LANG"
            and isinstance(node.ctx, ast.Load)
        ):
            self.references.append(
                LangReference(
                    file=self.file,
                    line=node.lineno,
                    property=node.attr,
                )
            )
        self.generic_visit(node)

def test_must_pass_with_all_valid_key():
    references = []
    folder = Path.cwd() / 'src' / 'selenium_wrapper'
    lang_files = list(folder.rglob('*.lang'))
    assert lang_files, 'No `*.lang` files found'
    for file in folder.rglob('*.py'):
        try:
            script = file.read_text(encoding='utf-8')
            tree = ast.parse(script, filename=str(file))
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        visitor = LangVisitor(file)
        visitor.visit(tree)
        references.extend(visitor.references)
    for lang_file in lang_files:
        paths = dotenv_values(lang_file)
        missing = [ref for ref in references if ref.property not in paths]
        assert not missing, (
            f'\nMissing properties in {lang_file}:\n'
                + '\n'.join(
                    f'{ref.file}:{ref.line}: LANG.{ref.property}'
                    for ref in missing
                )
        )
