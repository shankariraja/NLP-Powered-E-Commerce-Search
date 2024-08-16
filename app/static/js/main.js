document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsContainer = document.getElementById('results-container');

    // Trigger search on button click or Enter key press
    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    function performSearch() {
        const query = searchInput.value;
        console.log(`Debug: User query - ${query}`);

        if (query.trim() === '') {
            console.log('Debug: Empty query, search aborted.');
            return;
        }

        resultsContainer.innerHTML = 'Searching...';
        console.log('Debug: Initiated search with query:', query);

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => {
            console.log('Debug: Received response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Debug: Received data:', data);
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            resultsContainer.innerHTML = `An error occurred while searching: ${error.message}`;
        });        
    }

    function displayResults(data) {
        console.log('Debug: Displaying results:', data);

        resultsContainer.innerHTML = '';

        if (!Array.isArray(data) || data.length === 0) {
            console.log('Debug: No results found.');
            resultsContainer.innerHTML = 'No results found.';
            return;
        }

        const productsList = document.createElement('div');
        productsList.innerHTML = '<h2>Matching Products</h2>';
        
        data.forEach(product => {
            console.log('Debug: Processing product:', product);

            const productElement = document.createElement('div');
            productElement.className = 'product';
            productElement.innerHTML = `
                <h3>${product.product_name}</h3>
                <img src="${product.image_url}" alt="${product.product_name}" style="max-width: 100px;">
                <p>Price: $${product.final_price}</p>
                <p>Category: ${product.category_name}</p>
                <p>Brand: ${product.brand}</p>
                <p>Rating: ${product.rating} (${product.review_count} reviews)</p>
                <p>${product.description}</p>
            `;
            productsList.appendChild(productElement);
        });

        resultsContainer.appendChild(productsList);
        console.log('Debug: Results displayed successfully.');
    }
});
