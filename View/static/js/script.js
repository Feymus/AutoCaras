'use strict';

const myApp = angular.module('CargaDeImagenes', ['ngRoute']);
const url = "http://127.0.0.1:5000/";

myApp.controller('CargaImgsCtrl', function($scope, $http){

	$scope.send_dir = function(){

		var prefix = $scope.prefix;
		var energy = $scope.energy;
		var muestras = $scope.muestras;
    	var dir = $scope.name;

		var data_json = $.param({
			img_url:dir,
			ent_prefix:prefix,
			energy_pct:energy,
			num_entrenar:muestras
		});

		$http({
			url: url + "cargaimgs",
			method: "POST",
			data: data_json,
			headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
		}).then(function(response) {
		  var json_response = response['data'];
		  alert(json_response['msg'])
		});
  	};

});

myApp.controller('ReconocedorCtrl', function($scope, $http){

	$scope.send_dir = function(){

		var prefix = $scope.prefix;
		var energy = $scope.energy;
		var muestras = $scope.muestras;
    	var dir = $scope.name;

		var data_json = $.param({
			img_url:dir,
			ent_prefix:prefix,
			energy_pct:energy,
			num_entrenar:muestras
		});

		$http({
			url: url + "cargaimgs",
			method: "POST",
			data: data_json,
			headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
		}).then(function(response) {
		  var json_response = response['data'];
		  alert(json_response['msg'])
		});
  	};

});