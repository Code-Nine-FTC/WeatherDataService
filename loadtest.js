import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';

export let options = {
    vus: 200,
    duration: '1m',
};

export default function () {
    const endpoints = [
        'http://34.238.9.87:8000/alert_type',
        'http://34.238.9.87:8000/alert/all',
        'http://34.238.9.87:8000/alert_type/1',
		'http://34.238.9.87:8000/dashboard/station-history',
		'http://34.238.9.87:8000/parameter_type',
		'http://34.238.9.87:8000/weather_station/1',
		'http://34.238.9.87:8000/dashboard/alert-types',
		'http://34.238.9.87:8000/dashboard/alert-counts',
		'http://34.238.9.87:8000/dashboard/station-status',
		'http://34.238.9.87:8000/dashboard/measures-status',
    ];

    const res = http.get(endpoints[Math.floor(Math.random() * endpoints.length)]);
    check(res, {
        'status is 200': (r) => r.status === 200,
    });

    sleep(1);
}
