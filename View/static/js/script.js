'use strict';

const myApp = angular.module('CargaDeImagenes', ['ngRoute']);
const url = "http://127.0.0.1:5000/";

myApp.controller('CargaImgsCtrl', function($scope, $http){

	$scope.send_dir = function(){

    	var dir = $scope.name;
		var data_json = $.param({img_url:dir});

		$http({
			url: url + "cargaimgs",
			method: "POST",
			data: data_json,
			headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
		}).then(function(response) {
		  var json_response = response['data'];
		  alert(json_response['msg'])
		});
  }

});