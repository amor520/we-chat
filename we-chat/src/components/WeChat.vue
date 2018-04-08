<template>
  <div class="WeChat">
    <ve-bar :data="chartData" :settings="chartSettings" :extend="chartExtend" height="800px"></ve-bar>
  </div>
</template>

<script>
export default {
  name: "WeChat",
  data() {
    return {
      chartExtend:{},
      chartData: {},
      chartSettings: {},
    };
  },
  created() {
    setInterval(this.init, 5000);
    this.init();
  },
  methods: {
    init: function() {
      let vm = this;
      this.$http.get("/static/data.json").then(
        response => {
          let list = response.data;
          let rows = [];
          vm.chartData = {
            columns: ["_id", "count"],
            rows: list,
          };
          vm.chartExtend = {
            series: {
              barWidth: 10,
            },
          };
          vm.chartSettings = {
            label: {
              normal: { show: true, position: "right", formatter: "{@count}" },
            },
            dataOrder: {
              label: "count",
              order: "desc",
            },
            itemStyle: {
              color: "red",
            },
            metrics: ["count"],
            dimension: ["_id"],
          };
        },
        response => {
          alert("服务器请求失败");
        }
      );
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
