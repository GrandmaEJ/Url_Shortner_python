document.getElementById('shorten-form').addEventListener('submit', async function(event) {

    event.preventDefault();

    const form = event.target;

    const formData = new FormData(form);

    const formDataObj = {};

    formData.forEach((value, key) => (formDataObj[key] = value));

    const response = await fetch(form.action, {

        method: form.method,

        headers: {

            'Content-Type': 'application/json',

        },

        body: JSON.stringify(formDataObj),

    });

    const result = await response.json();

    if (result.status === 200) {

        document.getElementById('result').innerHTML = `

            <p>Shortened URL: <a href="${result.short_link}">${result.short_link}</a></p>

            <p>Original URL: ${result.redirect_link}</p>

            <p>Short ID: ${result.id}</p>

            <p>Creation Date: ${result.making_date_time}</p>

            <p>Expiration Date: ${result.expired_time}</p>

        `;

    } else {

        document.getElementById('result').innerHTML = `

            <p>Error: ${result.error}</p>

        `;

    }

});