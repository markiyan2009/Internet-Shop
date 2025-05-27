const url = 'http://127.0.0.1:8000/shop/home/categories/';

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('[id$="-category"]'); // Всі кнопки категорій

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const categoryId = button.id.split('-')[0]; // витягуємо ID
            
            fetch(`${url}?category=${categoryId}`)
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('products-container');
                    container.innerHTML = ''; // очищаємо старі товари

                    data.results.forEach(product => {
                        const productCard = `
                            <div class="col">
                                <div class="card" style="width: 18rem;">
                                    <img src="${product.image_url}" class="card-img-top">
                                    <div class="card-body">
                                        <p class="card-text">${product.name}</p>
                                        <ul class="list-group list-group-flush">
                                            <li class="list-group-item">${product.character || ''}</li>
                                        </ul>
                                        <a href="/shop/product/${product.pk}/" class="btn btn-primary">Go</a>
                                    </div>
                                </div>
                            </div>
                        `;
                        container.innerHTML += productCard;
                    });
                });
        });
    });
});





// var btnRandomPosts = document.getElementById('posts-random');
// const btnRandomDisc = document.getElementById('disc-random');
// const resultRandom = document.getElementById('result-random');


// document.addEventListener('DOMContentLoaded', (event) => { 
    
//     if (btnRandomPosts) { 
//         btnRandomPosts.addEventListener('click', function() {
//             resultRandom.innerHTML = '';


//             fetch('/social/home/random/?posts-btn=true')
//             .then(response => response.json())
//             .then(data => {
                
//                 data.results.forEach(item =>{
//                     console.log(item);
                    
//                     const rowRandom = document.createElement('div');
//                     rowRandom.className = 'row';
//                     const  postName = document.createElement('a');
//                     const postCommunity = document.createElement('a');
//                     const genre = document.createElement('p');
                    
//                     const postNameCol = document.createElement('div');
//                     postNameCol.className = 'col';
//                     const postCommunityCol = document.createElement('div');
//                     postCommunityCol.className = 'col';
//                     const genreCol = document.createElement('div');
//                     genreCol.className = 'col';
                    
                    
//                     postName.innerText =  item.name;
//                     postName.href =  'social/post/' + item.post_pk;
//                     postName.style = 'font-size: 30px;';
//                     postCommunity.innerText = item.community_name;
//                     postCommunity.href = 'community/' + item.community_pk;
//                     postCommunity.style = 'font-size: 30px;';
//                     genre.innerText = item.community_genre;
//                     genre.style = 'font-size: 30px;'

//                     postNameCol.appendChild(postName);
//                     postCommunityCol.appendChild(postCommunity);
//                     genreCol.appendChild(genre)
                    
//                     rowRandom.appendChild(postNameCol);
//                     rowRandom.appendChild(postCommunityCol);
//                     rowRandom.appendChild(genreCol);
                   
//                     resultRandom.appendChild(rowRandom);
//                 });
//             })
//             .catch(error => console.error('Помилка при пошуку:', error));
// })}});
        