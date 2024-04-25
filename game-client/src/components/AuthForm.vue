<template>
    <form action="action_page.php" method="post">
      <div class="imgcontainer">
      </div>

      <div class="container">
        <label for="uname"><b>Username</b></label>
        <input type="text" placeholder="Enter Username" name="uname" required>

        <label for="psw"><b>Password</b></label>
        <input type="password" placeholder="Enter Password" name="psw" required>

        <button type="submit" id="login">Login</button>
        <button type="submit" id="create">Create user</button>
      </div>
    </form>
</template>

<style scoped>
</style>
