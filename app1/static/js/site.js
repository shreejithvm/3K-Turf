// site.js (UI niceties)
document.addEventListener('DOMContentLoaded', function(){
document.querySelectorAll('.fade-up').forEach((el,i)=>{
setTimeout(()=>el.classList.add('show'), 60*i);
});


const cart = document.getElementById('cartCount');
if(cart){
cart.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.25)' }, { transform: 'scale(1)' }], { duration: 550, easing:'ease-out' });
}
});


// small helper: update cart count from JS (if you plan ajax add-to-cart later)
function setCartCount(n){
const el = document.getElementById('cartCount');
if(!el) return; el.textContent = n; el.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.25)' }, { transform: 'scale(1)' }], { duration: 350 });
}



