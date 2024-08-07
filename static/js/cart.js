function addToCart(productId,quantity) {
  console.log("este es el id del producto: ", productId)

  console.log("la cantidad es : ", quantity)

  fetch(`/carro/agregar/${productId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ product_id: productId, quantity: quantity })
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Error al agregar el producto al carrito');
    }
  })
  .then(data => {
    // Actualiza la información del carrito en la interfaz de usuario
    updateCartInfo(data);
  })
  .catch(error => {
    console.error('Error al agregar el producto al carrito:', error);
  });
}

function getCookie(name) {
  // Función auxiliar para obtener el valor de la cookie CSRF
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue.pop() : '';
}

function updateCartInfo(data) {
  // // Actualizar el número de productos en el carrito
  // const cartCountElement = document.getElementById('cart-count');
  // cartCountElement.textContent = data.total_items;
  //
  // // Actualizar la tabla del carrito
  // const cartTableBody = document.querySelector('#cart-table tbody');
  // cartTableBody.innerHTML = '';
  //
  // if (data.items.length === 0) {
  //   // Mostrar mensaje de carrito vacío
  //   const emptyRowElement = document.createElement('tr');
  //   emptyRowElement.innerHTML = `
  //     <td colspan="5" class="px-4 py-3 text-center font-light text-gray-500 dark:text-gray-400">
  //       Tu carrito de compras está vacío.
  //     </td>
  //   `;
  //   cartTableBody.appendChild(emptyRowElement);
  // } else {
  //   // Generar las filas de la tabla con los productos del carrito
  //   for (const item of data.items) {
  //     const rowElement = document.createElement('tr');
  //     rowElement.innerHTML = `
  //       <td class="px-4 py-3">${item.name}</td>
  //       <td class="px-4 py-3 flex items-center">
  //         <a href="${item.subtract_url}" class="mr-2 text-gray-500 hover:text-gray-700">-</a>
  //         ${item.cantidad}
  //         <a href="${item.add_url}" class="ml-2 text-gray-500 hover:text-gray-700">+</a>
  //       </td>
  //       <td class="px-4 py-3">$${item.price}</td>
  //       <td class="px-4 py-3">$${item.subtotal}</td>
  //       <td class="px-4 py-3">
  //         <a href="${item.remove_url}" class="text-gray-500 hover:text-gray-700">
  //           <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  //             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
  //           </svg>
  //         </a>
  //       </td>
  //     `;
  //     cartTableBody.appendChild(rowElement);
  //   }
  // }
}
