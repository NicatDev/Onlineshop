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
      
        data.orderitems.forEach(function(item) {
            var liElement = document.createElement('li');
        
        
            liElement.innerHTML = `
                <div class="d-flex">
                    <div  class="thumb">
                        <img  src="${item.product.image}" alt="${item.product.name}">
                    </div>
                    <div  class="content">
                        <h6  class="title"><a href="#" >${item.product.name} </a></h6>
                        <span class="price">$29.00</span>
                    </div>
                    <div class="action" >
                        <input type="number" value="${item.quantity}" readonly>
                        <a href="#" id="${item.product.id}" class="remove"><i  class="fa-solid fa-trash-can"></i></a>
                    </div>
                </div>
            `;
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
        var badgeElements = $('i.icon-heart').next('.badge');
        badgeElements.each(function () {
            $(this).text(data.count.toString());
        });
        return data;
    } catch (error) {
        throw error;
    }
}


