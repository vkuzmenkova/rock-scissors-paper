<script>
import LeaderBoard from '../components/LeaderBoard.vue'


export default {
  methods: {
    goToLeaderboard() {
      this.$router.push('/leaderboard')
    },
  },
}

</script>


<template>
  <LeaderBoard/>
</template>

<style>

</style>
