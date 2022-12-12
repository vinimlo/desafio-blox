<template>
    <h1>Login</h1>
    <form @submit.prevent="sendUserRegistry">
        <label for="user-registry">CPF</label>
        <input type="text" name="user-registry" id="user-registry" v-model="userRegistry">

        <input type="submit" value="Entrar">
    </form>
    <div v-if="shouldCreateAccount">
        <h3>
            Você está registrado, mas ainda não possui uma conta!
        </h3>
        <router-link :to="{
            name: 'create-account',
            params: { userRegistry: userRegistry }
        }">
            <button>
                Criar Conta
            </button>
        </router-link>
    </div>
    <div v-if="shouldRegister">
        <h3>
            Você ainda não está registrado!
        </h3>
        <router-link to="/register">
            <button>
                Registrar
            </button>
        </router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
    name: 'LoginView',
    data() {
        return {
            userRegistry: '',
            shouldCreateAccount: false,
            shouldRegister: false
        }
    },
    methods: {
        sendUserRegistry() {
            axios.get(`http://localhost:5000/get_account/${this.userRegistry}`)
                .then((response: any) => {
                    let message = response.data.message;

                    if (message) {
                        switch (message) {
                            case 'Person does not exist.':
                                this.shouldRegister = true;
                                this.shouldCreateAccount = false;
                                break;
                            case 'Account does not exist.':
                                this.shouldRegister = false;
                                this.shouldCreateAccount = true;
                                break;
                        }
                    }
                    else {
                        localStorage.setItem('user_account', JSON.stringify(response.data));
                    }
                });
        }
    }
});
</script>

<style>

</style>