
document.addEventListener("DOMContentLoaded", () => {

   const getSalesData = async ()=> {
      await fetch('api/sales-data')
      .then(response => response.json())
      .then(data => {
         console.log('DATA::',data)
         renderChart(data); 
      })
      .catch(error => {
         console.error('Error fetching sales data:', error);
      });   
    }
   const renderChart= (data)=> {
      const months = data.map(object => object.month);
      let monthList=[]
      months.forEach(dateString=>{
         
         const date = new Date(dateString);
         const options = { month: 'long' }; 
         const monthName = new Intl.DateTimeFormat('en-US', options).format(date);
         monthList.push(monthName)
      })
      console.log('monthList::',monthList)
      const salesAmounts = data.map(obj => obj.total);

      const ctx = document.getElementById('myChart').getContext('2d');
      // console.log('ctx::',ctx)
      new Chart(ctx, {
          type: 'bar',
          data: {
              labels: monthList,
              datasets: [{
                  label: 'Monthly Sales',
                  data: salesAmounts,
                  backgroundColor: 'rgba(54, 162, 235, 0.2)',
                  borderColor: 'rgba(54, 162, 235, 1)',
                  borderWidth: 1
              }]
          },
          options: {
               scales: {
                  y: {
                      beginAtZero: true
                  }
              },
               responsive: false,
               maintainAspectRatio: false
          }
      });
  }
    //call getSalesData
    getSalesData()

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