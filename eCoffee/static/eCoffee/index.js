
document.addEventListener("DOMContentLoaded", () => {
   const likeBtns = document.querySelectorAll(".like-btn");
 
   likeBtns.forEach((btn) => {
     const productId = btn.dataset.productId;
     const heartIcon=document.querySelector(`.heart-icon-${productId}`)
     
     btn.addEventListener("click", async () => {

       try {
         const response = await fetch(`/likes/${productId}`, {
           method: "POST",
           headers: {
             "Content-Type": "application/json",
             "X-CSRFToken": csrfToken,
           },
           body: JSON.stringify({ productId: productId }),
         });

         if (!response.ok) {
           throw new Error("Network response was not ok");
         }    

         const data = await response.json();
         console.log("DATA::", data.liked); 
         
         if(data.liked){            
            heartIcon.classList.toggle('liked', data.liked);
         }
        
       } catch (error) {
         console.error("Error found::", error);
       }
     });
   });
 });