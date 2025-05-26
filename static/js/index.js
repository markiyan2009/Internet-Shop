const url = 'http://127.0.0.1:8000/shop/home/categories/'
async function getCategoriesLen(){

    const response = await fetch(url);
    var data1 = await response.json();
    return data1.results[data1.results.length - 1].categories_len
};



document.addEventListener('DOMContentLoaded', async () => {
    const categories_len = await getCategoriesLen();

    const categories_buttons = [];
    for (let i = 1; i <= categories_len; i++) {
        const button = document.getElementById(`${i}-category`);
        if (button) {
            categories_buttons.push(button);
        }
    }

    console.log(categories_buttons);

    categories_buttons.forEach(button =>{
        button.addEventListener('click', function() {

            fetch(url)
            .then(response => response.json())
            .then(data => {
                data.results.forEach(item =>{

                })
            })

        })
    })

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
        