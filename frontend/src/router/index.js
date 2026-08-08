import { createRouter, createWebHistory } from 'vue-router'  /// needed to be explained 


const routes = [
  {
    path:"/",
  },
]

const router = createRouter({
  history: createWebHistory(),                      
  routes
})

export default router