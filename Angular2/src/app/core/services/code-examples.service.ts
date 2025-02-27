
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})

export class CodeExamplesService
{
    public category_id: number;

    constructor(
        private http: HttpClient,
    ) { }

    public headers = new HttpHeaders({ 'Content-Type': 'application/json'});

    getCode(category_id: number): Observable<Object>
    {
        return this.http.get(environment.API_ENDPOINT + `/api/code/items/${category_id}`, { headers: this.headers })
    }

    getCodeExample(code_id: number): Observable<Object>
    {
        return this.http.get(environment.API_ENDPOINT + `/api/code/${code_id}`, { headers: this.headers })
    }

    getChecklistKbCodeItems(checklist_kb_id: number): Observable<Object>
    {
        return this.http.get(environment.API_ENDPOINT + `/api/code/items/requirements/${checklist_kb_id}`, { headers: this.headers })
    }

    createCodeExample(value: any): Observable<Object>
    {
        this.category_id = Number(localStorage.getItem("categorySelector"))
        return this.http.put(environment.API_ENDPOINT + `/api/code/new/${this.category_id}`, value, { headers: this.headers })
    }

    updateCodeExample(code_id: number, value: any): Observable<Object>
    {
        return this.http.put(environment.API_ENDPOINT + `/api/code/update/${code_id}`, value, { headers: this.headers })
    }

    deleteCodeExample(code_id: number): Observable<Object>
    {
        return this.http.delete(environment.API_ENDPOINT + `/api/code/delete/${code_id}`, { headers: this.headers })
    }

}