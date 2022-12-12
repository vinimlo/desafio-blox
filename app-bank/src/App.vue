<template>
  <nav>
    <div id="nav-text">
      <router-link :to="{ name: 'login' }" v-if="!userIsLogged">Login</router-link>
      <div v-if="userIsLogged">
        Logado como {{ username }}
        <a @click="logout()">(Sair)</a>
      </div>
    </div>
  </nav>
  <section id="main-content">
    <router-view />
  </section>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
  data() {
    return {
      userIsLogged: false,
      username: ''
    }
  },
  mounted() {
    if (localStorage.getItem('user_account')) {
      this.userIsLogged = true;
      this.username = JSON
        .parse(
          String(localStorage.getItem('user_account'))
        ).person_relation.name;
    }
    else {
      this.userIsLogged = false;
      this.username = '';
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('user_account');
      this.userIsLogged = false;
      this.username = '';
    },
  }
});
</script>

<style>
body {
  background-color: #150050;
  color: #FAFAFA;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

a,
h3,
span {
  color: #FAFAFA;
  font-weight: 600;
}

h3 {
  display: block;
}

#app {
  font-family: Poppins, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #FAFAFA;
  min-height: 100vh;
}

nav {
  background-color: rgba(0, 0, 0, 0.3);
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: end;
}

nav a {
  font-weight: bold;
  color: #FAFAFA;
  cursor: pointer;
  text-decoration: none;
}

#nav-text {
  width: fit-content;
  padding: 0 15px;
}

nav a.router-link-exact-active {
  text-decoration: underline;
}

.message-box {
  background-color: rgba(255, 255, 255, 0.1);
  width: 80%;
  height: 50px;
  border-radius: 8px;
  margin: 15px auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

form {
  width: 80%;
  max-width: 550px;
  margin: 0 auto;
}

label {
  font-weight: 800;
  float: left;
  padding: 15px 15px 0 15px;
}

input[type=text],
input[type=number] {
  background-color: rgba(255, 255, 255, 0.05);
  color: #FAFAFA;
  font-size: 1em;
  font-weight: 600;
  padding: 10px;
  height: 30px;
  border: none;
  border-radius: 8px;
  width: calc(100% - 20px);
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}

input[type=text]:focus,
input[type=number]:focus {
  border: none;
  box-shadow: none;
  outline: none;
}

input[type=submit] {
  background-color: #FB2576;
  color: #FAFAFA;
  font-weight: 700;
  height: 35px;
  border: none;
  border-radius: 8px;
  width: 100%;
  margin: 15px 0;
  cursor: pointer;
}

input[type=submit]:disabled {
  cursor: unset;
}

input[type=number]:disabled {
  color: rgba(255, 255, 255, 0.5);
}

input[type="date"] {
  width: calc(100% - 43px);
  display: block;
  position: relative;
  padding: 10px 35px 10px 8px;
  font-size: 1rem;
  font-family: monospace;
  border: none;
  border-radius: 8px;
  background:
    white url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='22' viewBox='0 0 20 22'%3E%3Cg fill='none' fill-rule='evenodd' stroke='%23688EBB' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' transform='translate(1 1)'%3E%3Crect width='18' height='18' y='2' rx='2'/%3E%3Cpath d='M13 0L13 4M5 0L5 4M0 8L18 8'/%3E%3C/g%3E%3C/svg%3E") right 1rem center no-repeat;
  background-color: rgba(255, 255, 255, 0.05);
  color: #FAFAFA;
  cursor: pointer;
}

input[type="date"]:focus {
  outline: none;
  border: none;
  box-shadow: none;
}

::-webkit-datetime-edit-month-field:hover,
::-webkit-datetime-edit-day-field:hover,
::-webkit-datetime-edit-year-field:hover {
  background: rgba(0, 120, 250, 0.1);
}

::-webkit-datetime-edit-text {
  opacity: 0;
}

::-webkit-clear-button,
::-webkit-inner-spin-button {
  display: none;
}

::-webkit-calendar-picker-indicator {
  position: absolute;
  width: 2.5rem;
  height: 100%;
  top: 0;
  right: 0;
  bottom: 0;

  opacity: 0;
  cursor: pointer;

  color: #FAFAFA;
  background: #FAFAFA;

}

input[type="date"]:hover::-webkit-calendar-picker-indicator {
  opacity: 0.05;
}

input[type="date"]:hover::-webkit-calendar-picker-indicator:hover {
  opacity: 0.15;
}

select {
  appearance: none;
  -moz-appearance: none;
  -webkit-appearance: none;
  background-color: transparent;
  border: none;
  width: 100%;
  padding: 0 1em 0 0;
  margin: 0;
  height: 35px;
  font-family: inherit;
  font-size: inherit;
  cursor: inherit;
  line-height: inherit;
  outline: none;
  border-radius: 8px;
  padding: 5px 5px;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  background-color: rgba(255, 255, 255, 0.05);
  color: #FFFFFF;
  background-image: url("assets/arrow-down.svg");
  background-position:
    calc(100% - 20px) calc(1em + 2px),
    calc(100% - 15px) calc(1em + 2px),
    calc(100% - 2.5em) 0.5em;
  background-size:
    10px 7px,
    10px 10px,
    1px 1.5em;
  background-repeat: no-repeat;
  transition: all 0.5s;
  text-overflow: ellipsis;
  text-align: center;
  overflow: hidden;
  white-space: nowrap;
}

select::-ms-expand {
  display: none;
}

.form-container {
  width: 100%;
  height: 100%;
  min-height: calc(100vh - 50px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-container-inner {
  background-color: rgba(0, 0, 0, 0.25);
  width: 80%;
  height: 500px;
  max-width: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border-radius: 8px;
}

.form-container-inner .extra-info {
  display: flex;
  flex-direction: column;
  align-items: start;
  width: 80%;
  max-width: 550px;
  justify-content: center;
}

.form-container-inner .extra-info span {
  padding-top: 5px;
}

.reload-btn {
  background: none;
  border: none;
  width: 28px;
  height: 28px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  font-size: 1em;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.module-container {
  min-height: 100px;
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  margin: 10px;
}

#main-content {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
