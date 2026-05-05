from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# --- Configuration & Mock Data ---
PRODUCTS = [
    {"id": 1, "name": "Classic Essential Tee", "price": 25.00, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=80"},
    {"id": 2, "name": "Premium Heavyweight", "price": 35.00, "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?auto=format&fit=crop&w=800&q=80"},
    {"id": 3, "name": "Organic Cotton V-Neck", "price": 28.00, "image": "https://images.unsplash.com/photo-1554568218-0f1715e72254?auto=format&fit=crop&w=800&q=80"},
]

# --- HTML Templates (Using Template Strings for single-file portability) ---

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InkStyle | Custom T-Shirts</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .tshirt-preview {
            transition: background-color 0.3s ease;
            position: relative;
            width: 300px;
            height: 350px;
            background-image: url('https://www.transparentpng.com/download/t-shirt/MQpY9P-t-shirt-free-download-transparent.png');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-900">
    <nav class="bg-white shadow-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex-shrink-0 flex items-center">
                    <a href="/" class="text-2xl font-bold text-indigo-600 tracking-tight">INK<span class="text-gray-900">STYLE</span></a>
                </div>
                <div class="hidden md:flex space-x-8">
                    <a href="/" class="text-gray-600 hover:text-indigo-600 font-medium">Home</a>
                    <a href="/shop" class="text-gray-600 hover:text-indigo-600 font-medium">Shop</a>
                    <a href="/customize" class="text-indigo-600 font-bold">Design Your Own</a>
                </div>
                <div class="flex items-center space-x-4">
                    <button class="text-gray-600 hover:text-indigo-600"><i class="fa-solid fa-cart-shopping"></i></button>
                    <button class="bg-indigo-600 text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-indigo-700">Login</button>
                </div>
            </div>
        </div>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer class="bg-gray-900 text-white py-12 mt-20">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p class="text-gray-400">&copy; 2024 InkStyle Custom Prints. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

HOME_PAGE = """
{% extends "base" %}
{% block content %}
<section class="relative bg-white overflow-hidden">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center py-20 px-4">
        <div class="md:w-1/2 mb-10 md:mb-0">
            <h1 class="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight mb-6">
                Your Style, <br><span class="text-indigo-600">Your Statement.</span>
            </h1>
            <p class="text-lg text-gray-600 mb-8 max-w-lg">
                High-quality custom t-shirt printing for individuals and teams. Express yourself with our easy-to-use designer.
            </p>
            <div class="flex space-x-4">
                <a href="/customize" class="bg-indigo-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-indigo-700 transition">Start Designing</a>
                <a href="/shop" class="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-bold hover:bg-gray-50 transition">View Catalog</a>
            </div>
        </div>
        <div class="md:w-1/2">
            <img src="https://images.unsplash.com/photo-1527719327859-c6ce80353573?auto=format&fit=crop&w=1000&q=80" alt="Hero T-shirt" class="rounded-2xl shadow-2xl">
        </div>
    </div>
</section>

<section class="bg-gray-50 py-20">
    <div class="max-w-7xl mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12">Our Best Sellers</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {% for product in products %}
            <div class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition">
                <img src="{{ product.image }}" class="h-64 w-full object-cover">
                <div class="p-6">
                    <h3 class="font-bold text-xl mb-2">{{ product.name }}</h3>
                    <p class="text-gray-600 mb-4">${{ "%.2f"|format(product.price) }}</p>
                    <a href="/customize" class="block text-center bg-gray-900 text-white py-2 rounded-lg font-semibold hover:bg-gray-800">Customize</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
"""

CUSTOMIZE_PAGE = """
{% extends "base" %}
{% block content %}
<div class="max-w-6xl mx-auto px-4 py-12">
    <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold">Interactive Studio</h1>
        <p class="text-gray-500 mt-2">Personalize your gear in real-time</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
        <!-- Visualizer -->
        <div class="bg-white p-8 rounded-2xl shadow-xl flex justify-center items-center min-h-[500px]">
            <div id="shirt-container" class="tshirt-preview bg-white flex flex-col justify-center items-center text-center p-12">
                <p id="preview-text" class="text-xl font-bold break-words max-w-[150px] mt-10"></p>
            </div>
        </div>

        <!-- Controls -->
        <div class="bg-white p-8 rounded-2xl shadow-xl">
            <h2 class="text-2xl font-bold mb-6">Customization Options</h2>
            
            <div class="mb-8">
                <label class="block text-sm font-medium text-gray-700 mb-3">Shirt Color</label>
                <div class="flex space-x-4">
                    <button onclick="changeColor('white')" class="w-10 h-10 rounded-full border-2 border-gray-300 bg-white hover:scale-110 transition"></button>
                    <button onclick="changeColor('#1a1a1a')" class="w-10 h-10 rounded-full bg-gray-900 hover:scale-110 transition"></button>
                    <button onclick="changeColor('#ef4444')" class="w-10 h-10 rounded-full bg-red-500 hover:scale-110 transition"></button>
                    <button onclick="changeColor('#3b82f6')" class="w-10 h-10 rounded-full bg-blue-500 hover:scale-110 transition"></button>
                    <button onclick="changeColor('#10b981')" class="w-10 h-10 rounded-full bg-emerald-500 hover:scale-110 transition"></button>
                </div>
            </div>

            <div class="mb-8">
                <label class="block text-sm font-medium text-gray-700 mb-3">Print Text</label>
                <input type="text" id="text-input" placeholder="Type your slogan..." 
                       class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 p-3 border">
            </div>

            <div class="mb-8">
                <label class="block text-sm font-medium text-gray-700 mb-3">Text Color</label>
                <div class="flex space-x-4">
                    <button onclick="changeTextColor('black')" class="w-8 h-8 rounded bg-black border border-gray-300"></button>
                    <button onclick="changeTextColor('white')" class="w-8 h-8 rounded bg-white border border-gray-300"></button>
                    <button onclick="changeTextColor('gold')" class="w-8 h-8 rounded bg-yellow-400 border border-gray-300"></button>
                </div>
            </div>

            <div class="border-t pt-6">
                <div class="flex justify-between items-center mb-6">
                    <span class="text-gray-600">Base Price:</span>
                    <span class="text-2xl font-bold">$25.00</span>
                </div>
                <button class="w-full bg-indigo-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-indigo-700 transition shadow-lg">
                    Add to Cart
                </button>
            </div>
        </div>
    </div>
</div>

<script>
    const textInput = document.getElementById('text-input');
    const previewText = document.getElementById('preview-text');
    const shirt = document.getElementById('shirt-container');

    textInput.addEventListener('input', (e) => {
        previewText.textContent = e.target.value;
    });

    function changeColor(color) {
        shirt.style.backgroundColor = color;
    }

    function changeTextColor(color) {
        previewText.style.color = color;
    }
</script>
{% endblock %}
"""

# --- Routes ---

@app.route('/')
def home():
    return render_template_string(HOME_PAGE, products=PRODUCTS[:3])

@app.route('/base')
def base():
    # Helper to return base for inheritance
    return render_template_string(BASE_LAYOUT)

@app.route('/shop')
def shop():
    return render_template_string(HOME_PAGE, products=PRODUCTS)

@app.route('/customize')
def customize():
    return render_template_string(CUSTOMIZE_PAGE)

# Inject base layout into all other templates manually for this demo environment
@app.context_processor
def inject_base():
    return {'base_layout': BASE_LAYOUT}

# Handle Template Inheritance manually for render_template_string
def render_page(template, **kwargs):
    # This is a simplified engine to simulate standard Flask template folder structure
    full_html = BASE_LAYOUT.replace('{% block content %}{% endblock %}', template.split('{% block content %}')[1].split('{% endblock %}')[0])
    return render_template_string(full_html, **kwargs)

@app.route('/')
def index():
    return render_page(HOME_PAGE, products=PRODUCTS)

@app.route('/shop')
def products_list():
    return render_page(HOME_PAGE, products=PRODUCTS)

@app.route('/customize')
def studio():
    return render_page(CUSTOMIZE_PAGE)

if __name__ == '__main__':
    app.run(debug=True)
