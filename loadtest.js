import http from 'k6/http';
import { sleep, check } from 'k6';
import { SharedArray } from 'k6/data';

export let options = {
    vus: 200,
    duration: '1m',
};

// Faz login 1x antes de começar o teste
export function setup() {
    const loginPayload = {
        username: 'admcodenine@gmail.com',
        password: 'adm2025',
    };

    const loginHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
    };

    const res = http.post('http://34.238.9.87:8000/auth/login', loginPayload, { headers: loginHeaders });

    check(res, {
        'login status is 200': (r) => r.status === 200,
    });

    const token = res.json('access_token');
    return { token };
}

export default function (data) {
    const endpoints = [
        'http://34.238.9.87:8000/alert_type/',
        'http://34.238.9.87:8000/alert/all',
        'http://34.238.9.87:8000/alert_type/1',
        'http://34.238.9.87:8000/dashboard/station-history/1',
        'http://34.238.9.87:8000/parameter_types/',
        'http://34.238.9.87:8000/stations/1',
        'http://34.238.9.87:8000/dashboard/alert-types',
        'http://34.238.9.87:8000/dashboard/alert-counts',
        'http://34.238.9.87:8000/dashboard/station-status',
        'http://34.238.9.87:8000/dashboard/measures-status',
    ];

    const authHeaders = {
        headers: {
            Authorization: `Bearer ${data.token}`,
        },
    };

    const res = http.get(endpoints[Math.floor(Math.random() * endpoints.length)], authHeaders);

    check(res, {
        'status is 200': (r) => r.status === 200,
    });

    sleep(1);
}
