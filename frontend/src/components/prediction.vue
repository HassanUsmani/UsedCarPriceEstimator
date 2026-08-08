<template >
  <div class="prediction_box" v-if="boxStatus">
    <p>Predicted Price: </p>
    <br>
    <p v-if="loading" class="loader"></p>
    <p v-else>{{predicted_value}}</p>
  </div>
</template>

<script>
export default {
    props : ['predicted_value','boxStatus','loading'],

}
</script>

<style>
.prediction_box{
    top: 30%;
    justify-self: center;
    position: fixed;
    background: rgb(245, 243, 243);
    width: 200px;
    height: 100px;
    border-radius: 10px;
    
    /* transform: translate(); */
}
.prediction_box p{
    font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 500;
}
.loader {
    width: 40px;
    height: 40px;
    border: 5px solid #ff3c3c;
    /* border-top: 5px solid #333; */
    color: red;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}
</style>