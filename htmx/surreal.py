from fasthtml.common import *
app,rt = fast_app()

@rt("/")
def get():
    return Titled('Surreal.js and FastHTML Demos',
        H2("Demo Links"),
        Ul(
            Li(A("Original Demo", href="/original")),
            Li(A("Real-time Search Filter", href="/search-demo")),
            Li(A("Animated Todo List", href="/todo-demo")),
            Li(A("Interactive Image Gallery", href="/gallery-demo"))
        )
    )

@rt("/original")
def get():
    return Titled('Surreal.js demo',
        H3("fadeOut()"),
        Safe('I fade <i>out</i> and <i>remove</i> my italics.'),
        AnyNow('i', 'await sleep(1000); e.fadeOut()'),
        Button('Click me to remove me.', On('e.fadeOut()')),

        H3("On()"),
        Div("I change color when clicked.",
            On("e.styles('background-color: lightblue');")),

        H3("Any()"),
        Style(".highlight { background-color: yellow; }"),
        Button("Button 1"), Button("Button 2"), Button("Button 3"),
        Any("button", "e.classToggle('highlight');"),

        H3("Prev()"),
        Input(type="text", placeholder="Type here"),
        Prev("e.value = e.value.toUpperCase();", event="input"),
    )

@rt("/search-demo")
def get():
    return Titled('Dynamic Search',
        Input(type="text", placeholder="Search...", id="search"),
        Div(id="results"),
        Any("#search", """
            let query = e.value;
            let results = await fetch(`/search?q=${query}`).then(r => r.text());
            document.getElementById('results').innerHTML = results;
        """, event="input")
    )

@rt("/search")
def get(q: str):
    items = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
    results = [item for item in items if q.lower() in item.lower()]
    return Ul(*[Li(item) for item in results])

@rt("/todo-demo")
def get():
    return Titled('Animated Todo List',
        Input(type="text", id="new-todo", placeholder="Add a todo"),
        Button("Add", id="add-btn"),
        Ul(id="todo-list"),
        Any("#add-btn", """
            let todo = document.getElementById('new-todo').value;
            if (todo) {
                let li = document.createElement('li');
                li.textContent = todo;
                li.style.opacity = '0';
                document.getElementById('todo-list').appendChild(li);
                e.fadeIn(li);
                document.getElementById('new-todo').value = '';
            }
        """),
        Any("#todo-list li", "e.fadeOut().then(() => e.remove())")
    )

@rt("/gallery-demo")
def get():
    images = ["https://picsum.photos/200/300", "https://picsum.photos/200/301", "https://picsum.photos/200/302"]
    return Titled('Interactive Image Gallery',
        Div(id="gallery", *[Img(src=img) for img in images]),
        Style("""
            #gallery { display: flex; justify-content: space-around; }
            #gallery img { width: 200px; height: 200px; object-fit: cover; cursor: pointer; }
            #modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); }
            #modal img { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 90%; max-height: 90%; }
        """),
        Div(id="modal", *[Img(id="modal-img")]),
        Any("#gallery img", """
            let modal = document.getElementById('modal');
            let modalImg = document.getElementById('modal-img');
            modalImg.src = e.src;
            e.fadeIn(modal);
        """),
        Any("#modal", "e.fadeOut()")
    )

serve(host="127.0.0.1", port=5000)