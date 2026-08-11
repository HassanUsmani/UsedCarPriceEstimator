<template >
  <div class="prediction_box" v-if="boxStatus" :class="{active: loading === false}">
    <div v-if="loading">
        <p>Predicting...</p>
        <p class="loader"></p>
    </div>
    <div v-else>
        <p>Predicted Price: </p>
        <span>₹ {{Math.round(predicted_value / 100) * 100}}</span>
        <p>Estimated RMSE: </p>
        <span>₹ {{Math.round(166836.49453108816 / 100) * 100}}</span>
    </div>
    
  </div>
</template>

<script>
export default {
    props : ['predicted_value','boxStatus','loading'],

}
</script>

<style>
.prediction_box{
    z-index: 2;
    top: 40%;
    left: 50%;
    justify-self: center;
    position: fixed;
    background: rgb(245, 243, 243);
    width: 200px;
    height: 150px;
    border-radius: 10px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    position: absolute;
    transform: translate(-50%,-60%);
}
.prediction_box p{
    font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 500;
    font-size: 18px;
    padding-top: 15px;
}

.loader {
    width: 40px;
    height: 40px;    
    right: 40%;
    position: fixed;
    display: flex;
    transition: opacity 0.75s, visibility 0.75s;
  
}

.loader::after{
    content: "";
    animation: loading 0.75s ease infinite;
    width: 32px;
    height: 30px;
    border: 5px solid #ddd;
    border-radius:50%;
    border-top-color: #4285F4;
}
.prediction_box.active{
    background-color: #e2fbea;
    color: #09963c;
    border: 5px solid #74c28f;
}
/* bbf7d0 */
@keyframes loading {
    from {
        transform: rotate(0turn);
    }

    to {
        transform: rotate(1turn);
    }
}
</style>