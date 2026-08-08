<template>
    <form @submit.prevent='Predict()' v-if="showForm">
        <div class="maindiv">
            <h2>Used Car Value Estimator</h2>
            <label>Brand</label>
            <div @click="dropBrand()" class='dropdown-box' :class="{active : dropDownbrand == true}">
                <div class="selected-item">
                    <input type="text" readonly :value="selectedBrand">
                </div>
                <div class="dropdown">
                    <div class="search-input">
                        <input type="text">
                    </div>
                    <ul >
                        <li class="dropdown-item active">Select</li>
                        <li v-for="Brand in brands" :key="Brand" class="dropdown-item" value="Toyota" @click="selectBrand($event,Brand)">{{Brand}}</li>
                    </ul>
                </div>
            </div>
            <label>Model</label>
            <div @click="dropModel()" class='dropdown-box' :class="{active : dropDownmodel == true}">
                <div class="selected-item">
                    <input type="text" readonly :value="selectedModel">
                </div>
                <div class="dropdown">
                    <ul >
                        <li v-for="(Model,index) in models[brand]" :key="index" class="dropdown-item" @click="selectModel($event,Model)">{{Model}}</li>
                    </ul>
                    <ul v-if="modelLoaded">
                        <li class="not-selected">please select the brand first.</li>
                    </ul>
                </div>
            </div>

            <label for="">Engine</label>
            <div @click="dropEngine()" class="dropdown-box" :class="{active : dropDownengine == true}">
                <div class="selected-item">
                    <input type="text" readonly :value='selectedEngine'>
                </div>
                <div class="dropdown">
                    <ul>
                        <li @click="selectEngine(e, Engine)" v-for="Engine in engine_array" :key ="Engine" class="dropdown-iem">{{Engine}}</li>
                    </ul>
                    <ul>
                        <li class="not-selected" v-if="engineLoaded">please select the above credentials</li>
                    </ul>
                </div>
                
            </div>
            
        
            <label for="">km_driven</label>    
            <input type="text" v-model="km_driven" >

            <label for="">vehicle_age</label>    
            <input type="text" v-model="vehicle_age" >

            <label for="">mileage</label>    
            <input type="text" v-model="mileage" >
            
            <label for="">Fuel Type</label>
            <div @click="dropFuel()" class="dropdown-box" :class ="{active: dropDownFuel == true}">
                <div class="selected-item"> 
                    <input type="text" :value="selectedFuel" readonly>
                </div> 
                <div class="dropdown">
                    <ul>
                        <li @click="selectFuel(e, Fuel)" v-for="Fuel in fuels" :key="Fuel" class="dropdown-item ">{{Fuel}}</li>
                    </ul>
                    <ul>
                        <li class="not-selected" v-if="fuelLoaded">please select the above credentials</li>
                    </ul>
                </div>
            </div>
            <label for="">Transmission Type</label>
            <div @click="dropTransmission()" class="dropdown-box" :class ="{active: dropDownTransmission == true}">
                <div class="selected-item"> 
                    <input type="text" :value="selectedTransmission" readonly>
                </div> 
                <div class="dropdown">
                    <ul>
                        <li @click="selectTransmission(e, trans)" v-for="trans in transmission" :key="trans" class="dropdown-item ">{{trans}}</li>
                    </ul>
                    <ul>
                        <li class="not-selected" v-if="transLoaded">please select the above credentials</li>
                    </ul>
                </div>
            </div>

            <button class="submit" type="submit">Predict</button>

       </div>
    </form>

</template>

<script>
export default {
    data(){
        return{
            dropDownbrand:false,
            dropDownmodel:false,
            dropDownengine : false,
            dropDownFuel:false,
            dropDownTransmission:false,
            predicted:false,
            showForm:true,

            engineLoaded : true,
            modelLoaded : true,
            fuelLoaded : true,
            transLoaded : true,

            selectedBrand : 'Select',
            selectedModel : 'Select',
            selectedEngine : 'Select',
            selectedFuel : 'Select',
            selectedTransmission : 'Select',

            model : '',
            brand : '',
            fuel_type : '',
            transmission_type : '',
            engine : '',
            km_driven : 0,
            mileage : 0,
            vehicle_age : 0,

            brands : ["Toyota","Renault","Ford","Volkswagen","BMW","Volvo","Maruti","Skoda","Jaguar","Mahindra","Datsun",
                "Mercedes-Benz","Honda","Porsche","Hyundai","Audi","Jeep","Tata"],


            models : {
                "Toyota":['Innova','Fortuner','Camry','Yaris'],
                "Renault":['Duster','KWID'],
                "Ford":['Ecosport','Aspire','Figo','Endeavour','Freestyle'],
                "Volkswagen":['Vento','Polo'],
                "BMW":['5','3','X5','X1','7'],
                "Volvo":['not considering'],  // 'S90','XC','XC90','XC60'
                "Maruti":['Alto','Wagon R','Swift','Ciaz','Baleno','Swift Dzire','Ignis','Vitara','Celerio',
                    'Ertiga','Eeco','Dzire VXI','XL6','S-Presso','Dzire LXI','Dzire ZXI'],
                "Skoda":['Rapid','Superb','Octavia'],
                "Jaguar":['XF','F-PACE','XE'],
                "Mahindra":['Bolero','XUV500','KUV100','Scorpio','Marazzo','KUV','Thar','XUV300','Alturas'],
                "Datsun":['RediGo','GO','redi-GO'], // Not Confirmed whether to add or not
                "Mercedes-Benz":['C-Class','E-Class','GL-Class','S-Class','CLS','GLS'],
                "Honda":['City','Amaze','CR-V','Jazz','Civic','WR-V','CR'],
                "Porsche":['Cayenne','Maccan','Panamera'],
                "Hyundai":['Grand','Verna','i20','Creta','Santro','Venue','Elantra','Tucson'],
                "Audi":['A4','A6','Q7'],
                "Jeep":["not considering"],
                "Tata":['Tiago','Safari','Nexon','Hexa','Tigor']
            },
            fuels : [],
            transmission : [],
            engine_array :[]
        }
        
    },
    
    methods :{ 
        Predict(){
            if(this.brand && this.model && this.engine && this.km_driven && 
            this.vehicle_age && this.mileage && this.fuel_type && this.transmission_type){
                this.loading(true)
                const data = {
                    brand : this.brand,
                    model : this.model,
                    vehicle_age : this.vehicle_age,
                    km_driven : this.km_driven,
                    mileage : this.mileage,
                    fuel_type : this.fuel_type,
                    transmission_type : this.transmission_type,
                    engine : this.engine
                }
                console.log('if-block')
                fetch('http://localhost:8000/post' ,{
                    method : "POST",
                    headers : {
                    'content-type':'application/json'
                    }, body : JSON.stringify(data)
                }).then(response => {
                    if(!response.ok){
                        throw new Error ("Invalid Error")
                    }
                    return response.json()
                }).then(result => {console.log(result),this.sendPrediction(result)})
                  .catch(err => {console.log(err.message)})
                this.loading(false)
                  
            }else{

                console.log('else-block')
            }
        },
        dropBrand(){
            if(this.dropDownbrand){
                this.dropDownbrand = false
            }else{
                this.dropDownbrand = true 
                this.dropDownmodel = false  
                this.dropDownengine = false
                this.dropDownFuel = false
                this.dropDownTransmission = false
            }
        },
        dropModel(){
            if(this.dropDownmodel){
                this.dropDownmodel = false
            }else{
                if(this.brand){
                    this.modelLoaded = false
                }
                this.dropDownmodel = true
                this.dropDownbrand = false
                this.dropDownengine = false
                this.dropDownFuel = false
                this.dropDownTransmission = false
            }
        },
        dropEngine(){
            if(this.dropDownengine){
                this.dropDownengine = false
            }else{
                this.dropDownengine = true 
                this.dropDownbrand = false 
                this.dropDownmodel = false 
                this.dropDownFuel = false 
                this.dropDownTransmission = false
            }
            if(this.dropDownengine){
                
                fetch(`http://localhost:8000/engine/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}`,{
                    method : "GET"
                }).then(response => {
                    if(!response.ok){
                        throw new Error ("Request Failed")
                    }
                    this.engineLoaded = false
                    return response.json()
                    
                }).then(result => {this.engine_array = result, console.log(result)})
                  .catch(err => {console.log(err.message), this.engineLoaded = true})
                  
            }
        },
        dropFuel(){
            if(this.dropDownFuel){
                this.dropDownFuel = false
            }else{
                this.dropDownFuel = true 
                this.dropDownbrand = false 
                this.dropDownmodel = false 
                this.dropDownengine = false
                this.dropDownTransmission = false
            }
            if(this.dropDownFuel){
                fetch(`http://localhost:8000/fuel/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}/${encodeURIComponent(this.engine)}`,{
                    method : "GET"
                }).then(response => {
                    if(!response.ok){
                        throw new Error ("Request Failed")
                    }
                    this.fuelLoaded = false
                    return response.json()
                }).then(result => this.fuels = result)
                  .catch(err => {console.log(err.message), this.fuelLoaded = true})
            }
        },
        dropTransmission(){
            if(this.dropDownTransmission){
                this.dropDownTransmission = false
            }else{
                this.dropDownTransmission = true 
                this.dropDownFuel = false 
                this.dropDownbrand = false 
                this.dropDownmodel = false
                this.dropDownengine = false 
            }
            if(this.dropDownTransmission){
                fetch(`http://localhost:8000/trans/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}/${encodeURIComponent(this.engine)}`,{
                    method : "GET",
                   
                }).then(response => {
                    if(!response.ok){
                        throw new Error("Request Failed")
                    }
                    this.transLoaded=false
                    return response.json()
                })
                  .then(result => this.transmission = result)
                  .catch(err => {console.log(err.message),this.transLoaded=true})
            }
        },
        selectBrand(e, brand){
            if(this.selectedBrand != brand){    
                this.ResetAfterBrand()
            }
            this.selectedBrand = brand
            this.brand = brand
        },
        selectModel(e, model){
            if(this.selectedModel != model){
                this.ResetAfterModel()
            }
            this.selectedModel = model
            this.model = model
        },
        selectEngine(e, engine){
            if(this.selectedEngine != engine){
                this.ResetAfterEngine()
            }
            this.selectedEngine = engine 
            this.engine = engine
        },
        selectkm_driven(e, km){
            this.km_driven = km
        },
        selectFuel(e, fuel){
            this.selectedFuel = fuel 
            this.fuel_type = fuel
        },
        selectTransmission(e, transmission){
            this.selectedTransmission = transmission
            this.transmission_type = transmission
        },
        ResetAfterBrand(){
            this.selectedModel = 'Select'
            this.model = ''
            this.ResetAfterModel()
        },
        ResetAfterModel(){
            this.engine_array = []
            this.selectedEngine = 'Select'
            this.engine = ''  
            this.ResetAfterEngine()
        },
        ResetAfterEngine(){
            this.fuels = []
            this.transmission = []
            this.selectedFuel = 'Select'
            this.selectedTransmission = 'Select'          
            this.fuel_type = ''
            this.transmission_type = ''
        },
        sendPrediction(res){
            this.$emit('prediction', res)
        },
        // showPredictionbox(){
        //     this.$emit('close')
        // },
        loading(status){
            this.$emit('loading',status)
        }
    }
}
</script>

<style>

input{
    justify-content: left;
    width: 80%;
    padding: 5px;
    border-radius: 5px;
    outline: none;
}
label{
    width: 400px;
    background-color: aquamarine;
    text-align: left;
    padding: 5px;
    margin: 3px;
    display: inline-block;
    font-size: 20px;
    font-weight: 200;

}
.maindiv h2{
    /* background-color: cornsilk; */
    padding: 15px 2px;
}
/* .maindiv label{
    display: inline-block;
} */
.maindiv .dropdown-box{
    align-items: center;
    
}

.maindiv button{
    background-color: aqua;
    width: 100px;
    height: 40px;
    border-radius: 8px;
    margin: 5px;
}
.maindiv button:hover{
    cursor: pointer;
}
form{
    /* background: mediumslateblue;  */
    /* border-color: blue; */
    width: 500px;
    height: 700px;
    /* border-color: rgb(143, 161, 62);
    border-width: 10px; */
    background-color: rgba(136, 218, 218, 0.934);
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 7px;
    /* text-align: center; */
}
.dropdown-box label{
    text-align: left;
    background-color: azure;
}

*{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    /* width: 100%; */
    /* padding-left: 10px;
    padding-right: 10px;    */
}
.dropdown-box .selected-item{
    /* border: 1px solid rgb(160, 158, 158); */
    width: 100%;
}

.dropdown-box input{
    width: 80%; 
    border :1px solid rgb(160, 200, 200);
    padding-left: 0px;
    padding-right: 0px;
    outline: none;
    border-radius: 5px;
    padding: 5px;
    color: rgb(119, 101, 22);
}
.dropdown-box .selected-item{
    position: relative;
}
.dropdown-box .selected-item::after{ /**after pseudo class */
    content: '';
    width: 3px;
    height: 3px;
    border: 2px solid rgb(200,182,100);
    border-color: transparent green green transparent;
    position: absolute;
    top: 50%;
    right: 12%;
    transform: translateY(-70%) rotate(45deg);
    
}
.dropdown-box{
    width: 100%;
    /* margin-right: 200px; */
    /* background-color: blueviolet; */
    position: relative;
    align-items: center;
    /* justify-self: center; */
}
.dropdown-box .selected-item, .dropdown-box .selected-item input{
    cursor: pointer;
}
.dropdown-box .dropdown{
    box-shadow: 0 5px 15px rgb(0, 0,0, 15%);
    border-radius:  5px;
    max-height: 100px;
    overflow-y: auto;
    overflow-x: hidden;
    display: none;
    position: absolute;
    z-index: 99;
    background-color: rgb(231, 229, 229);
    width: 400px;
    justify-self: center;
    /* justify-self: center; */
}
.dropdown-box.active .dropdown{
    display:block;
}
.dropdown-box .dropdown ul{
    /* justify-content: left; */
    list-style: none;
    align-items: center;
}
.dropdown-box .dropdown .search-input{
    margin: 7px 5px 0px 5px;
    padding-top: 7px;
    
}
.dropdown-box .dropdown ul li{
    /* justify-self: left; */
    padding: 2px 5px;
    cursor: pointer;
    /* width: 100%; */
}
.dropdown-box .dropdown ul li:hover{
    color: blue;
    background-color: rgba(196, 196, 196, 0.407);
}
.dropdown-box .dropdown ul li.active{
    background-color: rgb(160, 200, 200);
    color: purple;
    
}
.selectDropdown select{
    /* background-color: darkblue; */
    width: 400px;
    display: inline-block;
    height: 30px;
    outline: none;
    
}
.dropdown-box .dropdown .not-selected:hover{
    cursor:default;
    background-color: rgb(231, 229, 229);
    color:red;
}
.dropdown-box .dropdown .not-selected{
    color: red;
    font-size: 14px;
    font-weight: 100;
    /* padding-top: 5px; */
}
</style>