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
                        <li v-for="Brand in brands" :key="Brand" class="dropdown-item" value="Toyota" @click="selectBrand(Brand)">{{Brand}}</li>
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
                        <li v-for="(Model,index) in models[brand]" :key="index" class="dropdown-item" @click="selectModel(Model)">{{Model}}</li>
                    </ul>
                    <ul v-if="modelLoaded">
                        <li class="not-selected">please select the brand first.</li>
                    </ul>
                </div>
            </div>

            <label for="">Engine (cc)</label>
            <div @click="dropEngine()" class="dropdown-box" :class="{active : dropDownengine == true}">
                <div class="selected-item">
                    <input type="text" readonly :value='engine' placeholder="Select">
                </div>
                <div class="dropdown">
                    <ul>
                        <li @click="selectEngine(Engine)" v-for="Engine in engine_array" :key ="Engine" class="dropdown-iem">{{Engine}}</li>
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
                        <li @click="selectFuel(Fuel)" v-for="Fuel in fuels" :key="Fuel" class="dropdown-item ">{{Fuel}}</li>
                    </ul>
                    <ul>
                        <li class="not-selected" v-if="fuelLoaded">please enter the above details first.</li>
                    </ul>
                </div>
            </div>

            <label for="">mileage</label>    
            <input type="number" min="1" v-model.number="mileage" @keydown='preventExponent' step="0.01" @blur="checkMileage" placeholder="Ex: 12.6" @focus="reqFieldsmil" :readonly="checkMileagereqflag">
            <p v-if="mileageMessage" :class="mileageMessagetype === 'warning'? 'warning-message' : 'error-message'">{{mileageMessage}}</p>

            <label for="">vehicle_age</label>    
            <input type="number" min='1' v-model.number="vehicle_age" @keydown='preventExponent' @blur="checkVehicle_age" placeholder="Ex: 9" @focus="reqFieldsveh_age" :readonly="veh_agereqflag">
            <p v-if="vehicle_ageMessage" :class="vehicle_ageMessagetype === 'warning'? 'warning-message':'error-message'">{{vehicle_ageMessage}}</p>

            <label for="">km_driven</label>    
            <input type="number"  min="100" v-model.number="km_driven" @keydown='preventExponent' placeholder="Ex: 50000" @blur="checkKm_driven" @focus="reqFieldskm" :readonly="km_drivenreqflag">
            <p v-if="km_drivenMessage" :class="km_drivenMessagetype === 'warning'? 'warning-message':'error-message'">{{km_drivenMessage}}</p>

            <label for="">Transmission Type</label>
            <div @click="dropTransmission()" class="dropdown-box" :class ="{active: dropDownTransmission == true}">
                <div class="selected-item"> 
                    <input type="text" :value="transmission_type" placeholder="Select" readonly>
                </div> 
                <div class="dropdown">
                    <ul>
                        <li @click="selectTransmission(trans)" v-for="trans in transmission" :key="trans" class="dropdown-item ">{{trans}}</li>
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

            submitted:false,

            engineLoaded : true,
            modelLoaded : true,
            fuelLoaded : true,
            transLoaded : true,

            mileageMessage : '',
            mileageMessagetype : '',
            checkMileagereqflag : false,

            km_drivenMessage : '',
            km_drivenMessagetype : '',
            km_drivenreqflag : false,

            vehicle_ageMessage : '',
            vehicle_ageMessagetype : '',
            veh_agereqflag : false,
            
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
        async Predict(){
            await this.checkMileage()
            await this.checkVehicle_age()
            this.checkKm_driven()
            if (this.km_drivenMessagetype == 'error' || this.mileageMessagetype == 'error' || this.vehicle_ageMessagetype == 'error'){
                alert ("Check the input values")
                return 
            }
            if (this.brand && this.model && this.engine && this.fuel_type && this.vehicle_age
                && this.km_driven && this.mileage && this.transmission_type){
                    this.loading(true)
                    try {
                        const data = {
                            brand : this.brand,
                            model : this.model,
                            engine : this.engine, 
                            fuel_type : this.fuel_type,
                            vehicle_age : this.vehicle_age,
                            km_driven : this.km_driven,
                            mileage : this.mileage,
                            transmission_type : this.transmission_type
                        }
                        const response = await fetch("http://localhost:8000/predict",{
                            method : "POST",
                            headers : {
                                "content-type":"application/json",
                            },   body : JSON.stringify(data)
                        })
                        if(!response.ok){
                            console.log(response)
                            throw new Error ("Request failed")
                        }
                        const result = await response.json()
                        this.sendPrediction(result)
                        this.submitted = true 
                        this.loading(false)
                        
                    } 
                    catch(err){
                        console.log(err.message)
                    }
                }
                else{
                    alert ("Enter the all the details")
                }
        },
        dropBrand(){
            if(this.dropDownbrand){
                this.dropDownbrand = false
            }else{
                this.dropDownstatus()
                this.dropDownbrand = true 
            }
        },
        dropModel(){
            if(this.dropDownmodel){
                this.dropDownmodel = false
            }else{
                if(this.brand){
                    this.modelLoaded = false
                }
                this.dropDownstatus()
                this.dropDownmodel = true
            }
        },
        async dropEngine(){
            if(this.dropDownengine){
                this.dropDownengine = false
            }else{
                try {
                const response = await fetch(`http://localhost:8000/engine/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}`)
                if(!response.ok){
                    console.log(this.engineLoaded)
                    throw new Error("Request failed")
                }
                const result = await response.json()
                this.engine_array = result 
                this.engineLoaded = false 
                this.dropDownstatus()
                
                }
                catch (err){
                    console.log(err.message)
                }
                finally {
                    this.dropDownengine = true  
                }

            }
        },
        async dropFuel(){
            if(this.dropDownFuel){
                this.dropDownFuel = false
            }else{
                try {
                    const response = await fetch(`http://localhost:8000/fuel/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}/${encodeURIComponent(this.engine)}`)
                    if(!response.ok){
                        throw new Error("Request failed")
                    }
                    const result = await response.json()
                    this.fuelLoaded = false 
                    this.fuels = result 
                    this.dropDownstatus()  
                }
                catch(err){
                    console.log(err.message)
                }
                finally {
                    this.dropDownFuel = true
                }
            }
        },
        async dropTransmission(){
            if(this.dropDownTransmission){
                this.dropDownTransmission = false
            }else{
                try {
                    const response = await fetch(`http://localhost:8000/trans/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}/${encodeURIComponent(this.engine)}`)
                    if(!response.ok){
                        throw new Error ("Request failed")
                    }
                    const result = await response.json()
                    this.transmission = result 
                    this.dropDownFuel = false 
                    this.dropDownbrand = false 
                    this.dropDownmodel = false
                    this.dropDownengine = false 
                    this.transLoaded = false
                }
                catch (err){
                    console.log(err.message)
                } finally {
                    this.dropDownTransmission = true 
                }
            }
        },
        async checkMileage(){
            this.checkMileagereqflag = false
            if(this.engine && this.mileage){
                try {
                    const response = await fetch(
                        `http://localhost:8000/mileage/${encodeURIComponent(this.engine)}`
                    )
                    if(!response.ok){
                        throw new Error("Request Failed")
                    }
                    const res = await response.json()
                    if(this.mileage > 40){
                        this.mileageMessage = "The entered mileage is too high for a realistic vehicle"
                        this.mileageMessagetype = "error"
                        return
                    }
                    if(this.mileage > Math.round(res.max + 2) || this.mileage < Math.round(res.min - 2)){
                        this.mileageMessage = "The mileage is unusual for this type of vehicle."
                        this.mileageMessagetype = "warning"
                        return 
                    }
                    this.mileageMessage = ''
                    this.mileageMessagetype = ''
                }
                catch (err){
                    console.log(err.message)
                }
            }
        },reqFieldsmil(){
            if(!this.engine){
                this.checkMileagereqflag = true
                this.mileageMessage = "please enter the above details first."
                this.mileageMessagetype = "error"
            }else{
                this.checkMileagereqflag = false
                this.mileageMessage = ""
                this.mileageMessagetype = ""
            }
        },
        async checkVehicle_age(){
            this.veh_agereqflag = false
            if(this.brand && this.model){
                try {
                    const response = await fetch(`http://localhost:8000/model_start_year/${encodeURIComponent(this.brand)}/${encodeURIComponent(this.model)}`)
                
                    if(!response.ok){
                        throw new Error("Request Failed")
                    }
                    const result = await response.json()
                    const currentYear = new Date().getFullYear()
                    if(this.vehicle_age > currentYear - result){
                        this.vehicle_ageMessage = 'The entered vehicle age is not valid for the selected model. Please check your input.'
                        this.vehicle_ageMessagetype = 'error'
                    }else{
                        this.vehicle_ageMessage = ''
                        this.vehicle_ageMessagetype = ''
                    }
                }
                catch(err){
                    console.log(err.message)
                }
            }
        },
        reqFieldsveh_age(){
            if(!this.brand || !this.model){
                this.veh_agereqflag = true
                this.vehicle_ageMessage = 'please enter the above details first.'
                this.vehicle_ageMessagetype = 'error'
            }else{
                this.checkveh_ageflagEmpty = false
                this.vehicle_ageMessage = ''
                this.vehicle_ageMessagetype = ''
            }
        },
        checkKm_driven(){
            this.km_drivenreqflag = false
            if (this.vehicle_age && this.km_driven){
                const kmPeryear = this.km_driven / this.vehicle_age 
                if (kmPeryear < 2000 ) {
                    this.km_drivenMessage = 'The vehicle has unusually low kilometers driven for its age.'
                    this.km_drivenMessagetype = 'warning' 
                }else if (kmPeryear >= 2000 && kmPeryear < 29000){
                    this.km_drivenMessage = ''
                    this.km_drivenMessagetype = ''                    
                }else if (kmPeryear >= 29000 && kmPeryear < 35000){
                    this.km_drivenMessagetype = 'warning' 
                    this.km_drivenMessage = 'The vehicle has unusually high kilometers driven for its age.'
                }else {
                    this.km_drivenMessagetype = 'error'
                    this.km_drivenMessage = "Too high for the vehicle's age."
                }
            }
        },
        reqFieldskm(){
            if(!this.vehicle_age){
                this.km_drivenMessagetype = 'error'
                this.km_drivenMessage = 'please enter the above details first.'
                this.km_drivenreqflag = true
            }else{
                this.km_drivenreqflag = false 
                this.km_drivenMessagetype = ''
                this.km_drivenMessage = ''
            }
        },
        selectBrand(brand){
            if(this.brand != brand){    
                this.ResetAfterBrand()
            }
            this.brand = brand
        },
        selectModel(model){
            if(this.model != model){
                this.ResetAfterModel()
            }
            this.model = model
        },
        selectEngine(engine){
            if(this.engine != engine){
                this.ResetAfterEngine()
            }
            this.engine = engine
        },
        selectkm_driven(km){
            this.km_driven = km
        },
        selectFuel(fuel){
            this.fuel_type = fuel
        },
        selectTransmission(transmission){
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
            this.warningStatus()
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
        },
        dropDownstatus(){
            this.dropDownFuel = false 
            this.dropDownbrand = false 
            this.dropDownmodel = false 
            this.dropDownengine = false
            this.dropDownTransmission = false
        },
        warningStatus(){
            this.mileageMessage = ''
            this.mileageMessagetype = ''
            this.checkMileagereqflag = false
            this.km_drivenMessage = ''
            this.km_drivenMessagetype = ''
            this.km_drivenreqflag = false
            this.vehicle_ageMessage = ''
            this.vehicle_ageMessagetype = ''
            this.veh_agereqflag = false
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
    background-color: #F8FAFC;
}
input[type="number"] {
    border: 1px solid #B8CCCC;
    box-sizing: border-box;
    color: rgb(119, 101, 22);
}
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
label{
    width: 80%;
    background-color: #f1f3faf0;
    text-align: left;
    padding: 5px;
    margin: 3px;
    display: inline-block;
    font-size: 20px;
    font-weight: 200;
}
.maindiv h2{
    padding: 15px 2px;
    color: #285656;
}

.maindiv button{
    background-color: #3d6fdacb;
    color: white;
    font-size: 16px;
    font-weight: bold;
    width: 100px;
    height: 40px;
    border-radius: 8px;
    margin: 5px;
    box-shadow: 2px 2px 20px rgba(0, 0, 0, 0.284);
}
.maindiv button:hover{
    cursor: pointer;
    background-color: #1D4ED8;
}
.maindiv {
    width: 100%;
}
form{
    width: min(90%,500px);
    height: auto;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    border:2px Solid #CBD5E1;
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
    border :1px solid #CBD5E1;
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
    background-color: #F1F7F7;
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
    background-color: #D8EBEB;
}
.dropdown-box .dropdown .not-selected:hover{
    cursor:default;
    background-color: #F1F7F7;
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
}
</style>