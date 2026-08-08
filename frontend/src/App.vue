<template>
  <div class="parent">
  <Form  @prediction='handlePrediction' @loading='handleLoading'/>
  <predictionBox :predicted_value = "prediction" :boxStatus="showPredictionbox" :loading='isloading'/>
  </div>
</template>

<script>
import Form from "./components/Form.vue"
import predictionBox from "./components/prediction.vue"
export default{
  
  data(){
    return {
      data:true,
      prediction : null,
      showPredictionbox : false,
      isloading : false,
      loadingStartTime : 0
      }
  },
  name: 'App',
  components: {Form, predictionBox},
  methods: {
    
    handlePrediction(result){
      
      
      const elapsed = Date.now() - this.loadingStartTime 
      const RandomMinimum = Math.random() * 1000 + 1000

      const remaining = Math.max(0, RandomMinimum - elapsed)

      setTimeout(() => {
        this.isloading = false, 
        this.prediction = result
      },remaining)
    },
    handleLoading(status){
      if(status){
        this.loadingStartTime = Date.now()
        this.showPredictionbox = true
        this.isloading = true
      }
    }
    
  }
}

</script>

<style>   
#app {
  font-family: Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px; 
  justify-items: center;
}
body{
  margin :0;
  /* background: #eee; */
  
}
.parent{
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
