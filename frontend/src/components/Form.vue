<template>
    <form @submit.prevent='Predict()'>
        <div class="overlay" v-if="submitted" @click="Rebring()">

        </div>
        <div class="maindiv" :class="{disable : submitted === true}">
            <h2>Used Car Value Estimator</h2>
            <label>Brand</label>
            <div @click="dropBrand()" class='dropdown-box' :class="{active : dropDownbrand == true}">
                <div class="selected-item">
                    <input type="text" readonly :value="brand" placeholder="Select">
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
                    <input type="text" readonly :value="model" placeholder="Select">
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
                    <input type="text" readonly :value='engine' placeholder="Select">
                </div>
                <div class="dropdown">
                    <ul>
                        <li @click="selectEngine(e, Engine)" v-for="Engine in engine_array" :key ="Engine" class="dropdown-iem">{{Engine}}</li>
                    </ul>
                    <ul>
                        <li class="not-selected" v-if="engineLoaded">please enter the above details first.</li>
                    </ul>
                </div>
                
            </div>
            
            <label for="">Fuel Type</label>
            <div @click="dropFuel()" class="dropdown-box" :class ="{active: dropDownFuel == true}">
                <div class="selected-item"> 
                    <input type="text" :value="fuel_type" placeholder="Select" readonly>
                </div> 
                <div class="dropdown">
                    <ul>
                        <li @click="selectFuel(e, Fuel)" v-for="Fuel in fuels" :key="Fuel" class="dropdown-item ">{{Fuel}}</li>
                    </ul>
                    <ul>
                        <li class="not-selected" v-if="fuelLoaded">please enter the above details first.</li>
                    </ul>
                </div>
            </div>

            <label for="">vehicle_age</label>    
            <input type="number" min='1' v-model.number="vehicle_age" @keydown='preventExponent' @blur="checkVehicle_age" placeholder="Ex: 9">
            <p v-if="invalidAgeflag" class="error-message">The entered vehicle age is not valid for the selected model. Please check your input.</p>

            <label for="">km_driven</label>    
            <input type="number"  min="100" v-model.number="km_driven" @keydown='preventExponent' placeholder="Ex: 50000" @blur="checkKm_driven">
            <p v-if="km_drivenwarnflag" class="warning-message">{{km_drivemsg}}</p>
            <p v-if="km_drivenrejflag" class="error-message">Too high for the vehicle's age.</p>


            <label for="">mileage</label>    
            <input type="number" min="1" v-model.number="mileage" @keydown='preventExponent' step="0.1" @blur="checkMileage" placeholder="Ex: 12.6">
            <p v-if="checkMileageflagEmpty" class="error-message">please enter the above details first.</p>
            <p v-if="checkMileageflag" class="warning-message">The mileage is unusual for this type of vehicle</p>

            <label for="">Transmission Type</label>
            <div @click="dropTransmission()" class="dropdown-box" :class ="{active: dropDownTransmission == true}">
                <div class="selected-item"> 
                    <input type="text" :value="transmission_type" placeholder="Select" readonly>
                </div> 
                <div class="dropdown">
                    <ul>
                        <li @click="selectTransmission(e, trans)" v-for="trans in transmission" :key="trans" class="dropdown-item ">{{trans}}</li>
                    </ul>
                    <ul>
                        <li class="not-selected" v-if="transLoaded">please enter the above details first.</li>
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
            km_drivenrejflag : false,
            km_drivenwarnflag : false,

            checkMileageflag : false,
            checkMileageflagEmpty : false,
            km_drivenflag : false,
            invalidAgeflag:false,
            km_drivemsg : '',
            
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
                this.km_drivenflag = false
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
                this.km_drivenwarnflag = false
                this.km_drivenrejflag = false
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
                this.km_drivenwarnflag = false
                this.km_drivenrejflag = false
                
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
                this.km_drivenflag = false
                this.km_drivenwarnflag = false
                this.km_drivenrejflag = false
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
            if(this.engine && this.fuel_type && this.mileage){
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
                    }
                }
                catch (err){
                    console.log(err.message)
                }
            }
            else if (!(this.engine && this.fuel_type)){
                this.checkMileageflagEmpty = true
            }
        },
        async checkVehicle_age(){
            this.invalidAgeflag = false
            if(this.brand && this.model){
                try {
                const response = await fetch(`http://localhost:8000/vehicle_age/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}`)
            
                if(!response.ok){
                    throw new Error("Request Failed")
                }
                console.log(response)
                const result = await response.json()
                const currentYear = new Date().getFullYear()
                console.log(currentYear - result)
                console.log(currentYear)
                console.log(result)
                if(this.vehicle_age > currentYear - result){
                    this.invalidAgeflag = true
                    this.vehicle_age = ''
                    console.log(currentYear - result)
                    console.log('inside-if')
                }
                }
                catch(err){
                    console.log(err.message)
                }
            }
        },
        checkKm_driven(){
            this.km_drivenwarnflag = false
            this.km_drivenrejflag = false
            if (this.vehicle_age && this.km_driven){
                const kmPeryear = this.km_driven / this.vehicle_age 
                if (kmPeryear < 3000 ) {
                    this.km_drivemsg = 'The vehicle has unusually low kilometers driven for its age.'
                    this.km_drivenwarnflag = true
                }else if (kmPeryear >= 3000 && kmPeryear < 27000){
                    this.km_drivenrejflag = false
                    this.km_drivenwarnflag = false                    
                }else if (kmPeryear >= 27000 && kmPeryear < 32000){
                    this.km_drivenwarnflag = true 
                    this.km_drivemsg = 'The vehicle has unusually high kilometers driven for its age.'
                }else {
                    this.km_drivenrejflag = true
                    this.km_drivemsg = "Too high for the vehicle's age."
                }
                console.log(kmPeryear)
            }else{
                this.km_driven = ''
                this.km_drivemsg = 'Please enter the above details.'
            }
        },
        selectBrand(e, brand){
            if(this.brand != brand){    
                this.ResetAfterBrand()
            }
            this.brand = brand
        },
        selectModel(e, model){
            if(this.model != model){
                this.ResetAfterModel()
            }
            this.model = model
        },
        selectEngine(e, engine){
            if(this.engine != engine){
                this.ResetAfterEngine()
            }
            this.engine = engine
        },
        selectkm_driven(e, km){
            this.km_driven = km
        },
        selectFuel(e, fuel){
            this.fuel_type = fuel
        },
        selectTransmission(e, transmission){
            this.transmission_type = transmission
        },
        ResetAfterBrand(){
            this.model = ''
            this.ResetAfterModel()
        },
        ResetAfterModel(){
            this.engine_array = []
            this.engine = ''  
            this.ResetAfterEngine()
        },
        ResetAfterEngine(){
            this.fuels = []
            this.transmission = []      
            this.fuel_type = ''
            this.transmission_type = ''
            this.km_driven = ''
            this.mileage = ''
            this.vehicle_age = ''
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
            }
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
.error-message {
    color: red;
    font-size: 13px;
}
.warning-message {
    color: #D97706;
    font-size: 13px;
}
input{
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
    width: 80%;
    background-color: aquamarine;
    text-align: left;
    padding: 5px;
    margin: 3px;
    display: inline-block;
    font-size: 20px;
    font-weight: 200;
}
.maindiv h2{
    padding: 15px 2px;
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
    width: 90%;
    max-width: 500px;
    height: auto;
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
*{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.dropdown-box input{
    border :1px solid rgb(160, 200, 200);
    color: rgb(119, 101, 22);
}
.dropdown-box .selected-item{
    position: relative;
}
.dropdown-box .selected-item::after{
    content: '';
    width: 3px;
    height: 3px;
    border-color: transparent green green transparent;
    border-style: solid;
    border-width: 2px;
    position: absolute;
    top: 50%;
    right: 12%;
    transform: translateY(-70%) rotate(45deg);
}
.dropdown-box{
    width: 100%;
    position: relative;

}
.dropdown-box .selected-item, .dropdown-box .selected-item input{
    cursor: pointer;
}
.dropdown-box .dropdown{
    box-shadow: 0 5px 15px rgb(0, 0,0, 15%);
    border-radius: 5px;
    max-height: 100px;
    overflow-y: auto;
    overflow-x: hidden;
    display: none;
    position: absolute;
    z-index: 99;
    background-color: rgb(231, 229, 229);
    width: 80%;
    left: 10%;
}
.dropdown-box.active .dropdown{
    display:block;
}
.dropdown-box .dropdown ul{
    list-style: none;
}
.dropdown-box .dropdown ul li{
    padding: 2px 5px;
    cursor: pointer;
    overflow-wrap: break-word;
}
.dropdown-box .dropdown ul li:hover{
    color: rgb(107, 107, 255);
    background-color: rgba(209, 209, 209, 0.407);
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
}

@media (max-width: 480px) {
    label {
        font-size: 18px;
    }
    .maindiv button {
        width: 90px;
        height: 35px;
        font-size: 14px;
    }
}
@media (max-width: 300px) {
    label,
    input,
    .dropdown-box .selected-item input,
    .dropdown-box .dropdown {
        width: 90%;
    }

    .dropdown-box .dropdown {
        left: 5%;
    }
}
</style>