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
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
