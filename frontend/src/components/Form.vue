<template>
    <form @submit.prevent='Predict()'>
        <div class="overlay" v-if="submitted" @click="Rebring()">

        </div>
        <div class="maindiv" :class="{disable : submitted === true}">
            <h2>Used Car Value Estimator</h2>
            <label>Brand</label>
            <div @click="dropBrand()" class='dropdown-box' :class="{active : dropDownbrand == true}">
                <div class="selected-item">
                    <input type="text" readonly :value="selectedBrand">
                </div>
                <div class="dropdown">
                    <ul >
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
                        <li class="not-selected" v-if="engineLoaded">please enter the above detais first.</li>
                    </ul>
                </div>
                
            </div>
            
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
                        <li class="not-selected" v-if="fuelLoaded">please enter the above detais first.</li>
                    </ul>
                </div>
            </div>

            <label for="">km_driven</label>    
            <input type="number"  min="100" v-model.number="km_driven" @keydown='preventExponent'>

            <label for="">vehicle_age</label>    
            <input type="number" min='1' v-model.number="vehicle_age" @keydown='preventExponent'>

            <label for="">mileage</label>    
            <input type="number" min="1" v-model.number="mileage" @keydown='preventExponent' step="0.1" @blur="checkMileage">
            <p v-if="checkMileageflagEmpty" style="color:red;">please enter the above details first.</p>
            <p v-if="checkMileageflag" style="color:#D97706;">The mileage is unusual for this type of vehicle</p>

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
                        <li class="not-selected" v-if="transLoaded">please enter the above detais first.</li>
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
            submitted:false,

            engineLoaded : true,
            modelLoaded : true,
            fuelLoaded : true,
            transLoaded : true,
            checkMileageflag : false,
            checkMileageflagEmpty : false,

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
            km_driven : '',
            mileage : '',
            vehicle_age : '',

            brands : ["Toyota","Renault","Ford","Volkswagen","BMW","Maruti","Skoda","Jaguar","Mahindra","Datsun",
                "Mercedes-Benz","Honda","Porsche","Hyundai","Audi","Jeep","Tata"],


            models : {
                "Toyota":['Innova','Fortuner','Camry'],
                "Renault":['Duster','KWID'],
                "Ford":['Ecosport','Aspire','Figo','Endeavour','Freestyle'],
                "Volkswagen":['Vento','Polo'],
                "BMW":['5','3','X5','X1','7','X3'],
                "Maruti":['Alto','Wagon R','Swift','Ciaz','Baleno','Swift Dzire','Ignis','Vitara','Celerio',
                    'Ertiga','Eeco'],
                "Skoda":['Rapid','Superb','Octavia'],
                "Jaguar":['XF'],
                "Mahindra":['Bolero','XUV500','KUV100','Scorpio','Marazzo','KUV','Thar'],
                "Datsun":['GO'],
                "Mercedes-Benz":['C-Class','E-Class','GL-Class','S-Class'],
                "Honda":['City','Amaze','CR-V','Jazz','Civic','WR-V'],
                "Hyundai":['Grand','Verna','i20','Santro','Venue','Elantra','Creta','i10'],
                "Audi":['A4','A6','Q7'],
                "Jeep":["Compass"],
                "Tata":['Tiago','Safari','Nexon','Hexa','Tigor','Harrier']
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
                this.submitted = true
            }else{
                alert('Enter all the required information')
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
                this.checkMileageflag = false
                this.checkMileageflagEmpty = false
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
                this.checkMileageflag = false
                this.checkMileageflagEmpty = false
            }
        },
        async dropEngine(){
            if(this.dropDownengine){
                this.dropDownengine = false
            }else{
                await fetch(`http://localhost:8000/engine/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}`,{
                    method : "GET"
                }).then(response => {
                    if(!response.ok){
                        throw new Error ("Request Failed")
                    }
                    this.engineLoaded = false
                    return response.json()
                    
                }).then(result => {this.engine_array = result, console.log(result)})
                  .catch(err => {console.log(err.message), this.engineLoaded = true})
                this.dropDownengine = true 
                this.dropDownbrand = false 
                this.dropDownmodel = false 
                this.dropDownFuel = false 
                this.dropDownTransmission = false
                this.checkMileageflag = false
                this.checkMileageflagEmpty = false
            }

        },
        async dropFuel(){
            if(this.dropDownFuel){
                this.dropDownFuel = false
            }else{
                await fetch(`http://localhost:8000/fuel/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}/${encodeURIComponent(this.engine)}`,{
                    method : "GET"
                }).then(response => {
                    if(!response.ok){
                        throw new Error ("Request Failed")
                    }
                    this.fuelLoaded = false
                    return response.json()
                }).then(result => this.fuels = result)
                  .catch(err => {console.log(err.message), this.fuelLoaded = true})
                this.dropDownFuel = true 
                this.dropDownbrand = false 
                this.dropDownmodel = false 
                this.dropDownengine = false
                this.dropDownTransmission = false
                this.checkMileageflag = false
                this.checkMileageflagEmpty = false
            }
        },
        async dropTransmission(){
            if(this.dropDownTransmission){
                this.dropDownTransmission = false
            }else{
                await fetch(`http://localhost:8000/trans/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}/${encodeURIComponent(this.engine)}`,{
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
                this.dropDownTransmission = true 
                this.dropDownFuel = false 
                this.dropDownbrand = false 
                this.dropDownmodel = false
                this.dropDownengine = false 
            }
        },
        async checkMileage(){
            this.checkMileageflag = false
            if(this.engine && this.fuel_type){
                try {
                    const response = await fetch(
                        `http://localhost:8000/mileage/${encodeURIComponent(this.engine)}`
                    )
                    if(!response.ok){
                        throw new Error("Request Failed")
                    }
                    const res = await response.json()
                    if(this.mileage > Math.round(res.max + 2) || this.mileage < Math.round(res.min - 2)){
                        this.checkMileageflag = true
                        console.log(Math.round(res.max + 2))
                        console.log(Math.round(res.min - 2))
                        console.log(res)
                        console.log(this.mileage)
                    }
                }
                catch (err){
                    console.log(err.message)
                }
            }
            else{
                this.checkMileageflagEmpty = true
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
            this.km_driven = ''
            this.mileage = ''
            this.vehicle_age = ''
            this.checkMileagemsg = ''
        },
        sendPrediction(pred){
            this.$emit('prediction', pred)
        },
        loading(status){
            this.$emit('loading',status)
        },
        Rebring(){
            if(this.submitted){
                this.submitted = false 
                this.$emit('close')
                console.log('inside-if')
            }
            console.log('outside-if')
        },
        preventExponent(event){
            if (event.key == 'e' | event.key == 'E'){
                event.preventDefault()
            }
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
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
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
.maindiv .dropdown-box{
    align-items: center;   
}

.maindiv button{
    background-color: rgba(93, 174, 142, 0.768);
    font-size: 16px;
    font-weight: bold;
    width: 100px;
    height: 40px;
    border-radius: 8px;
    margin: 5px;
    box-shadow: 2px 2px 20px rgba(0, 0, 0, 0.247);
}
.maindiv button:hover{
    cursor: pointer;
}
form{
    width: 500px;
    height: 740px;
    background-color: rgba(136, 218, 218, 0.934);
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 7px;
    position: relative;

}
.disable {
    cursor: default;
    opacity: 0.3;
}
.overlay{
    z-index: 1;
    position: absolute;
    inset: 0;
    background-color: transparent;
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
}
/* .dropdown-box .selected-item{
    width: 100%;
} */

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
    position: relative;
    align-items: center;

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
}
.dropdown-box.active .dropdown{
    display:block;
}
.dropdown-box .dropdown ul{
    list-style: none;
    align-items: center;
}
.dropdown-box .dropdown .search-input{
    margin: 7px 5px 0px 5px;
    padding-top: 7px;
    
}
.dropdown-box .dropdown ul li{
    padding: 2px 5px;
    cursor: pointer;
}
.dropdown-box .dropdown ul li:hover{
    color: rgb(107, 107, 255);
    background-color: rgba(209, 209, 209, 0.407);
}
.dropdown-box .dropdown ul li.active{
    background-color: rgb(160, 200, 200);
    color: purple;
}
.selectDropdown select{
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