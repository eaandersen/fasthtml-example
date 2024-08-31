from fasthtml.common import *

app = FastHTML(hdrs=(picolink, MarkdownJS(), HighlightJS()))


@app.route("/")
def get():
    title = "Code Snippet Example"
    code_text = open(__file__, "r").read()
    md = Div(
        f"""### Usage:
```python
{code_text}
```""",
        cls="marked",
    )
    return Title(title), Main(H1(title), md, cls="container")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
