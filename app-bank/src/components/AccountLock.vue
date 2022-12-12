<template>
  <div class="module-container">
    <h3>
      Bloqueio
    </h3>
    <div id="lock-container">
      <div class="button r" id="button-1">
        <input type="checkbox" class="checkbox" @change="lockAccount()" v-model="lock" />
        <div class="knobs"></div>
        <div class="layer"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'AccountLock',
  emits: ['lockedAccount'],
  data() {
    return {
      accountId: 0,
      lock: false
    }
  },
  mounted() {
    let account = JSON.parse(
      String(localStorage.getItem('user_account'))
    );
    this.accountId = account.id;
    axios.get(`http://localhost:5000/account/${this.accountId}`)
      .then((response: any) => {
        this.lock = !response.data.is_active;
      });
  },
  methods: {
    lockAccount() {
      let is_locked = this.lock;
      axios.patch(`http://localhost:5000/account/${this.accountId}`, {
        is_active: !is_locked
      })
        .then((response) => {
          this.$emit('lockedAccount', response.data.is_active);
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }
});
</script>

<style scoped>
* {
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

.knobs,
.layer {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.button {
  position: relative;
  top: 50%;
  width: 74px;
  height: 36px;
  margin: -20px auto 0 auto;
  overflow: hidden;
}

.button.r,
.button.r .layer {
  border-radius: 100px;
}

.checkbox {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  opacity: 0;
  cursor: pointer;
  z-index: 3;
}

.knobs {
  z-index: 2;
}

.layer {
  width: 100%;
  background-color: rgba(255, 255, 255, 0.1);
  transition: 0.3s ease all;
  z-index: 1;
}

/* Button 1 */
#button-1 .knobs:before {
  content: "Não";
  position: absolute;
  top: 4px;
  left: 4px;
  width: 20px;
  height: 10px;
  color: #fff;
  font-size: 10px;
  font-weight: bold;
  text-align: center;
  line-height: 1;
  padding: 9px 4px;
  background-color: #150050;
  border-radius: 50%;
  transition: 0.3s cubic-bezier(0.18, 0.89, 0.35, 1.15) all;
}

#button-1 .checkbox:checked+.knobs:before {
  content: "Sim";
  left: 42px;
  background-color: #FB2576;
}

#button-1 .checkbox:checked~.layer {
  background-color: rgba(255, 255, 255, 0.1);
}

#button-1 .knobs,
#button-1 .knobs:before,
#button-1 .layer {
  transition: 0.3s ease all;
}

#lock-container {
  padding: 15px 0;
}
</style>