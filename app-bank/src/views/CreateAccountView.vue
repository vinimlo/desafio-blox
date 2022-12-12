<template>
    <h1>Criar conta</h1>
    <label for="name">Nome: </label>
    <span id="name">{{ name }}</span>

    <label for="registry">CPF: </label>
    <span id="registry">{{ registry }}</span>

    <label for="birthdate">Data de Nascimento: </label>
    <span id="birthdate">{{ birthdate }}</span>

    <form @submit.prevent="createAccount">

        <label for="account-type">Tipo de conta</label>
        <select name="account-type" id="account-type" v-model="accountType">
            <option value="1">Conta Poupança</option>
            <option value="2">Conta Corrente</option>
        </select>

        <input type="submit" value="Entrar">
    </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
    name: 'CreateAccountView',
    props: {
        userRegistry: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            name: '',
            registry: '',
            birthdate: '',
            accountType: 0,
            userId: 0
        }
    },
    mounted() {
        this.registry = this.userRegistry;
        axios.get(`http://localhost:5000/person/${this.registry}`)
            .then((response: any) => {
                console.log(response.data);
                this.birthdate = response.data.birthdate.substring(0, 10);
                this.name = response.data.name;
                this.userId = response.data.id;
            });
    },
    methods: {
        createAccount() {
            let accountType = +this.accountType;
            let person_id = this.userId;

            axios.post('http://localhost:5000/account', {
                account_type: accountType,
                person_id: person_id
            })
                .then((response) => {
                    console.log(response);
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    }
});
</script>

<style>

</style>