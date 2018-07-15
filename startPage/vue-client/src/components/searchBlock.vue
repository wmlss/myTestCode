<template lang="html">
  <div id="searchBlock">
    <div class="weather-wrap">
      safd
    </div>
    <el-row class="search-wrap">
      <el-input placeholder="请输入内容"class="input-with-select">
        <el-select  class="search-select" v-model="selectEngine" size="medium" slot="prepend" placeholder="请选择">
          <el-option label="google" value="1" >google</el-option>
          <el-option label="百度" value="2">百度</el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </el-row>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      data: 'test',
      selectEngine: "1"
    }
  }
}
</script>

<style lang="css" scoped>
#searchBlock {
  width: 100%;
}
#searchBlock .weather-wrap {
  display: block;
  height: calc(250px - 40px);
}
.search-wrap .search-select {
  min-width: 100px;
  height: 40px;
}
</style>
