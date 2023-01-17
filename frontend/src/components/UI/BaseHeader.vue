<template>
  <header>
    <small><slot name="link"></slot></small>
    <h1><slot name="header"></slot></h1>
  </header>
</template>

<script>


export default {
  name: 'base-header',
  props: {
    href: { type: String },
  },
}
</script>

<style>

</style>