
import re


class Conversor_doc_type():
    """
    Conversor_doc_type class to convert between Markdown and HTML formats.

    Returns:
        _type_: _description_
    """
    def markdown_to_html(markdown_text):
        """Convert Markdown to HTML."""
        html_text = markdown_text

        # Convert headers
        html_text = re.sub(r"^#{6}\s(.*?)$", r"<h6>\1</h6>", html_text, flags=re.MULTILINE)
        html_text = re.sub(r"^#{5}\s(.*?)$", r"<h5>\1</h5>", html_text, flags=re.MULTILINE)
        html_text = re.sub(r"^#{4}\s(.*?)$", r"<h4>\1</h4>", html_text, flags=re.MULTILINE)
        html_text = re.sub(r"^#{3}\s(.*?)$", r"<h3>\1</h3>", html_text, flags=re.MULTILINE)
        html_text = re.sub(r"^#{2}\s(.*?)$", r"<h2>\1</h2>", html_text, flags=re.MULTILINE)
        html_text = re.sub(r"^#\s(.*?)$", r"<h1>\1</h1>", html_text, flags=re.MULTILINE)

        # Convert bold and italic
        html_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", html_text)
        html_text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", html_text)

        # Convert links
        html_text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', html_text)

        # Convert unordered lists
        html_text = re.sub(r"^\*\s(.*?)$", r"<ul><li>\1</li></ul>", html_text, flags=re.MULTILINE)

        # Convert paragraphs
        html_text = re.sub(r"^(?!<h[1-6]>|<ul>|<li>|<a>|<b>|<i>)(.*?)$", r"<p>\1</p>", html_text, flags=re.MULTILINE)

        return html_text

    def html_to_markdown(html_text):
        """Convert HTML to Markdown."""
        markdown_text = html_text

        # Convert headers
        markdown_text = re.sub(r"<h1>(.*?)</h1>", r"# \1", markdown_text)
        markdown_text = re.sub(r"<h2>(.*?)</h2>", r"## \1", markdown_text)
        markdown_text = re.sub(r"<h3>(.*?)</h3>", r"### \1", markdown_text)
        markdown_text = re.sub(r"<h4>(.*?)</h4>", r"#### \1", markdown_text)
        markdown_text = re.sub(r"<h5>(.*?)</h5>", r"##### \1", markdown_text)
        markdown_text = re.sub(r"<h6>(.*?)</h6>", r"###### \1", markdown_text)

        # Convert bold and italic
        markdown_text = re.sub(r"<b>(.*?)</b>", r"**\1**", markdown_text)
        markdown_text = re.sub(r"<i>(.*?)</i>", r"*\1*", markdown_text)

        # Convert links
        markdown_text = re.sub(r'<a href="(.*?)">(.*?)</a>', r"[\2](\1)", markdown_text)

        # Convert unordered lists
        markdown_text = re.sub(r"<ul><li>(.*?)</li></ul>", r"* \1", markdown_text)

        # Remove paragraph tags
        markdown_text = re.sub(r"<p>(.*?)</p>", r"\1", markdown_text)

        return markdown_text

### TO Open HTML view

# # import module
# import codecs

# # to open/create a new html file in the write mode
# f = open('GFG.html', 'w')

# # the html code which will go in the file GFG.html
# html_template = """
# <html>
# <head></head>
# <body>
# <p>Hello World! </p>

# </body>
# </html>
# """

# # writing the code into the file
# f.write(html_template)

# # close the file
# f.close()

# # viewing html files
# # below code creates a
# # codecs.StreamReaderWriter object
# file = codecs.open("GFG.html", 'r', "utf-8")

# # using .read method to view the html
# # code from our object
# print(file.read())








# # import module
# import webbrowser

# # open html file
# webbrowser.open('GFG.html')