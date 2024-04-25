<script>
export default {
  methods: {
    goToAuth() {
      this.$router.push('/auth')
    },
  },
}

</script>


<template>
    <div class="auth">
      <main>
        <AuthForm/>
      </main> 
    </div>
</template>
