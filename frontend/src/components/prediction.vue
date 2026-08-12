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
    background-color: #eeeff2;
    max-width: 200px;
    width:60%;
    height: auto;
    min-height: 150px;
    border-radius: 10px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    position: absolute;
    transform: translate(-50%,-60%);
}
.prediction_box p{
    font-weight: 500;
    font-size: 20px;
    padding-top: 15px;
}

.loader {
    width: 40px;
    height: 40px; 
    left: 50%;
    top: 50%;   
    position: absolute;
    display: flex;
    transform: translate(-50%, -50%);
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
    background-color: #e6fbedbd;
    color: #09963c;
    border: 2px solid #86bb99;
}
@keyframes loading {
    from {
        transform: rotate(0turn);
    }

    to {
        transform: rotate(1turn);
    }
}
@media (max-width: 480px) {
    .prediction_box p {
        font-size: 17px;
        /* width: 50%; */
    }
}
</style>