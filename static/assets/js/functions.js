function updateBasket(csrfToken,url) {
    
    const formData = {};  

    fetch(url, {
        method: 'POST', 
        body: JSON.stringify(formData),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        console.log(response);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        var ulElement = document.getElementById('orderitems');
        ulElement.innerHTML = ''
        console.log(data)

        var basketElements = document.querySelectorAll(".basketbadge");
        basketElements.forEach(function(element, index) {
            element.textContent = data.count;
        });
      
            console.log(data.orderitems.length,'>')
        data.orderitems.forEach(function(item) {
            // Create li element
            var liElement = document.createElement('li');
        
        
            liElement.innerHTML = `
                <div class="d-flex">
                    <div style="width:25%" class="thumb">
                        <img  src="${item.product.image}" alt="${item.product.name}">
                    </div>
                    <div style="text-align:left;display: flex;
                    flex-direction: column;
                    justify-content: space-between;width:65%" class="content">
                        <h6  class="title"><a href="single-product.html" >${item.product.name} </a></h6>
                        <span class="price">$29.00</span>
                    </div>
                    <div class="action" style="text-align:center;display: flex;
                    flex-direction: column;
                    justify-content: space-between;">
                        <input type="number" value="${item.quantity}">
                        <a href="#" id="${item.product.id}" class="remove"><i style="color:black !important; font-size:20px; padding-top:5px" class="fa-solid fa-trash-can"></i></a>
                    </div>
                </div>
            `;
            console.log(item.product.id,'000000000')
            ulElement.appendChild(liElement);
        });
        var liElement = document.createElement('li');
        
        
        liElement.innerHTML = `
        <div style="width:100%" class="d-flex">
        <a href="../auth/shopping" class="btn btn-contact" style="width:100%;color:white;padding:13px 50px !important">Ətraflı</a>
    </div>
        `;
        ulElement.appendChild(liElement);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}


async function fetchData(myurl) {
    try {
        const response = await fetch(myurl);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data, 'data');

        var badgeElements = $('i.icon-heart').next('.badge');
        console.log(badgeElements, '------------badges');
        badgeElements.each(function () {
            console.log(data.count, '------------');
            $(this).text(data.count.toString());
            console.log($(this));
        });
        return data;
    } catch (error) {
        console.error('Error:', error.message);
        throw error;
    }
}


