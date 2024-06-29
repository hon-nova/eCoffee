
document.addEventListener("DOMContentLoaded", () => {

  // Get the context of the canvas element where the chart will be rendered
  const ctx = document.getElementById('myChart').getContext('2d');

  const data ={
   labels: [
      {% for sale in monthly_sales %}
   ]
  }
    
  // Define the chart data and options
  var myChart = new Chart(ctx, {
      type: 'bar',  // Specify the type of chart (e.g., bar, line, pie, etc.)
      data: {
          labels: ['January', 'February', 'March', 'April', 'May'],  // Labels for x-axis
          datasets: [{
              label: 'Sales',  // Label for the dataset
              data: [12, 19, 3, 5, 2],  // Data points for the dataset
              backgroundColor: 'rgba(54, 162, 235, 0.2)',  // Background color for bars
              borderColor: 'rgba(54, 162, 235, 1)',  // Border color for bars
              borderWidth: 1  // Border width for bars
          }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: true  // Start y-axis at zero
              }
          }
      }
  });

  // 2. like or unlike
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