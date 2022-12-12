<template>
  <div v-if="userIsLogged">
    <div v-if="accountIsLocked" class="message-box">
      <span>
        Conta bloqueada. Não é possível realizar depositos/saques
      </span>
    </div>
    <div id="dashboard">
      <div class="dashboard-row">
        <div class="dashboard-col">
          <AccountLock @lockedAccount="displayLockMessage" />
        </div>
        <div class="dashboard-col">
          <AccountBalance ref="accountBalance" />
        </div>
      </div>
      <div class="dashboard-row">
        <div class="dashboard-col">
          <AccountDeposit @updateBalance="updateBalance" :isAccountLocked="accountIsLocked" />
        </div>
        <div class="dashboard-col">
          <AccountWithdrawal @updateBalance="updateBalance" :isAccountLocked="accountIsLocked" />
        </div>
      </div>
      <div class="dashboard-row">
        <div class="dashboard-col">
          <AccountTransactions />
        </div>
      </div>
    </div>
  </div>
  <div v-if="!userIsLogged" class="message-box">
    <span>
      Para ter acesso a sua conta, realize login.
    </span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import AccountBalance from '@/components/AccountBalance.vue'
import AccountDeposit from '@/components/AccountDeposit.vue'
import AccountLock from '@/components/AccountLock.vue'
import AccountTransactions from '@/components/AccountTransactions.vue'
import AccountWithdrawal from '@/components/AccountWithdrawal.vue'

export default defineComponent({
  name: 'HomeView',
  components: {
    AccountBalance,
    AccountDeposit,
    AccountLock,
    AccountTransactions,
    AccountWithdrawal
  },
  data() {
    return {
      accountIsLocked: false
    }
  },
  mounted() {
    if (this.userIsLogged) {
      let accountId = JSON.parse(
        String(localStorage.getItem('user_account'))
      ).id
      axios.get(`http://localhost:5000/account/${accountId}`)
        .then((response: any) => {
          this.accountIsLocked = !response.data.is_active
        });
    }
  },
  computed: {
    userIsLogged(): boolean {
      return (this.$root as any).userIsLogged;
    }
  },
  methods: {
    updateBalance() {
      (this.$refs.accountBalance as typeof AccountBalance).getBalance();
    },
    displayLockMessage(is_active: boolean) {
      this.accountIsLocked = !is_active;
    }
  }
});
</script>

<style scoped>
#dashboard {
  display: grid;
}

.dashboard-row {
  display: flex;
  flex-direction: row;
  width: 100%;
}

.dashboard-col {
  display: flex;
  flex-direction: column;
  width: 100%;
}

@media only screen and (max-width: 769px) {
  .dashboard-row {
    flex-direction: column;
  }
}
</style>