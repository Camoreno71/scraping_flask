from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def scrape_page():
    with sync_playwright() as p:
        # Iniciar el navegador y abrir una nueva página
        browser = p.chromium.launch(headless=False)  # Puedes poner headless=True para que no se vea el navegador
        page = browser.new_page()

        # Navegar a la URL deseada
        page.goto("https://elbaratillo.co/")

        p_element = page.query_selector('p.elementor-heading-title.elementor-size-default')
        text = p_element.inner_text()
        input_selector = 'input.hfe-search-form__input[type="search"]'
        print(input_selector)

        page.fill(input_selector, 'texto de búsqueda')

        button = page.query_selector('a.elementor-button.elementor-button-link.elementor-size-lg')
        if button:
            button.click() 
            page.wait_for_load_state('networkidle')
            h2_element = page.query_selector('h2.widget-title')
            h2_text = h2_element.text_content()
            print(h2_text)

    return f"<p>hola{text}</p>"

if __name__ == "__main__":
    app.run(debug=True)