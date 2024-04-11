function addWish(id,url,csrftoken) {
  console.log(id,'----------',url)
 
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'id':id,
        },

        headers: {
            'X-CSRFToken': csrftoken  
        },
        dataType: 'json',
        success: function (data) {
            if (data.status === 'success') {
    
        
          
                if (data.action === 'added') {
                  
                    $(`.product-${id}`).css('font-weight', '900');
                }
                else if(data.action === 'removed'){
                    
                    $(`.product-${id}`).css('font-weight', '400');
                }
                $('.wishbadge').text(data.len);
          
                if (!window.location.href.includes("/wish")) {
                
                Swal.fire({
                    icon: 'success',
                    title: 'Uğurla tamamlandı'
                })}else{
                    window.location.reload()
                }
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Xəta',
                    text: 'Bu özəllikdən istifadə etmək üçün hesaba daxil olmalısınız    !',
                    confirmButtonText: 'Tamam'
                })
            }
        },
        error: function () {
            alert('An unexpected error occurred.');
        }
    });
}


function remove_basket(id,url,csrftoken) {
   
      $.ajax({
          type: 'POST',
          url: url,
          data: {
              'id':id,
          },
  
          headers: {
              'X-CSRFToken': csrftoken  
          },
          dataType: 'json',
          success: function (data) {
              if (data.status === 'success') {
                $(`basket-div-${id}`).remove();
                  Swal.fire({
                      icon: 'success',
                      title: 'Uğurla tamamlandı'
                  })
              } else {
                  Swal.fire({
                      icon: 'error',
                      title: 'Xəta',
                      text: 'Bu özəllikdən istifadə etmək üçün hesaba daxil olmalısınız    !',
                      confirmButtonText: 'Tamam'
                  })
              }
          },
          error: function () {
              alert('An unexpected error occurred.');
          }
      });
  }



  function delete_order_item(id,url,csrftoken) {
   
  
      $.ajax({
          type: 'POST',
          url: url,
          data: {
              'orderitem_id':id,
          },
  
          headers: {
              'X-CSRFToken': csrftoken  
          },
          dataType: 'json',
          success: function (data) {
             if (data.success = 'success'){
                window.location.reload();
             }
          },
          error: function () {
              alert('An unexpected error occurred.');
          }
      });
  }
  