document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsContainer = document.getElementById('results-container');

    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    function performSearch() {
        const query = searchInput.value;
        if (query.trim() === '') return;

        resultsContainer.innerHTML = 'Searching...';

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            resultsContainer.innerHTML = 'An error occurred while searching.';
        });
    }

    function displayResults(data) {
        resultsContainer.innerHTML = '';

        if (data.products.length === 0) {
            resultsContainer.innerHTML = 'No results found.';
            return;
        }

        const resultsList = document.createElement('ul');
        data.products.forEach(product => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <h3>${product.product_name}</h3>
                <p>Price: $${product.final_price}</p>
                <p>Category: ${product.category_name}</p>
                <p>Brand: ${product.brand}</p>
                <p>Rating: ${product.rating} (${product.review_count} reviews)</p>
            `;
            resultsList.appendChild(listItem);
        });

        resultsContainer.appendChild(resultsList);

        if (data.suggested_keywords) {
            const keywordsElement = document.createElement('p');
            keywordsElement.innerHTML = `<strong>Suggested Keywords:</strong> ${data.suggested_keywords.join(', ')}`;
            resultsContainer.appendChild(keywordsElement);
        }
    }
});