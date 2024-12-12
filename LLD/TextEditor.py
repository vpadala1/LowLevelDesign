class CharacterStyle:
    """Flyweight class representing the intrinsic state of a character (style)."""
    def __init__(self, font_name, font_size, is_bold=False, is_italic=False):
        self.font_name = font_name
        self.font_size = font_size
        self.is_bold = is_bold
        self.is_italic = is_italic

    def __repr__(self):
        style = f"Font: {self.font_name}, Size: {self.font_size}, Bold: {self.is_bold}, Italic: {self.is_italic}"
        return style

class CharacterStyleFactory:
    """Factory class to create and manage the flyweight CharacterStyle objects."""
    _styles = {}

    @classmethod
    def get_style(cls, font_name, font_size, is_bold=False, is_italic=False):
        key = (font_name, font_size, is_bold, is_italic)
        if key not in cls._styles:
            cls._styles[key] = CharacterStyle(font_name, font_size, is_bold, is_italic)
        return cls._styles[key]

class Character:
    """Class representing a character with extrinsic state (position) and shared intrinsic state (style)."""
    def __init__(self, char, style, position):
        self.char = char
        self.style = style
        self.position = position

    def __repr__(self):
        return f"'{self.char}' at {self.position} with style [{self.style}]"

class Document:
    """Class representing the document containing characters."""
    def __init__(self):
        self.characters = []

    def add_character(self, char, style, position):
        character = Character(char, style, position)
        self.characters.append(character)

    def delete_character(self, position):
        self.characters = [c for c in self.characters if c.position != position]

    def read_line(self, line_number):
        # Simplified for this example; assumes each line has 10 characters.
        start = (line_number - 1) * 10
        end = start + 10
        line = [c for c in self.characters if start <= c.position < end]
        return ''.join(c.char for c in line)

class TextEditor:
    """Text editor interface for interacting with the document."""
    def __init__(self):
        self.document = Document()

    def add_text(self, text, style, start_position):
        for i, char in enumerate(text):
            self.document.add_character(char, style, start_position + i)

    def delete_text(self, position):
        self.document.delete_character(position)

    def display_line(self, line_number):
        return self.document.read_line(line_number)

# Example usage:
if __name__ == "__main__":
    editor = TextEditor()

    style1 = CharacterStyleFactory.get_style("Arial", 12, is_bold=True)
    style2 = CharacterStyleFactory.get_style("Times New Roman", 14)

    editor.add_text("Hello", style1, 0)
    editor.add_text("World", style2, 5)

    print("Line 1:", editor.display_line(1))

    editor.delete_text(6)  # Deletes 'W'

    print("Line 1 after deletion:", editor.display_line(1))
