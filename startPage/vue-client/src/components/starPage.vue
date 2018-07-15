<template>
  <div class="wrap">
    <el-row class="page-top border">
      <el-col class="border test" :span="7"></el-col>
      <el-col class="border" :span="10"><searchBlock></searchBlock></el-col>
      <el-col class="border test" :span="7"></el-col>
    </el-row>
    <el-row class="page-bottom" type="flex" justify="center">
      <el-col class="border test" :span="10">{{data}}<div class="grid-content bg-purple-dark"></div></el-col>
    </el-row>
  </div>
</template>

<script>
import searchBlock from './searchBlock.vue'

export default {
  name: 'HelloWorld',
  components: {
    searchBlock
  },
  data: function() {
    return {
      data: 'test'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.wrap {
  height: 100%;
  width: 100%;
}
.page-top {
  /* height: 500px; */
  margin-top: 60px;
}
.border {
  border: 1px solid black;
}
.test {
  height: 30px;
}
</style>
