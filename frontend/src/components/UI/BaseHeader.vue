<template>
  <header class="my-3">
    <div><slot name="link"></slot></div>
    <h1><slot name="header"></slot></h1>
    <div><slot name="extra"></slot></div>
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