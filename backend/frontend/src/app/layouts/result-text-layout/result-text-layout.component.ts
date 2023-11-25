import {
  ChangeDetectionStrategy,
  Component,
  Inject,
  TemplateRef,
} from '@angular/core';
import { ResultTextFacadeService } from './facade/result-text-facade.service';
import { filter, map, of, switchMap, tap } from 'rxjs';
import { GetResultTextDto } from '@hackaton-speech2text-glossary/dto';
import { NbDialogService } from '@nebular/theme';

@Component({
  selector: 'hackaton-speech2text-glossary-result-text-layout',
  templateUrl: './result-text-layout.component.html',
  styleUrls: ['./result-text-layout.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ResultTextLayoutComponent {
  readonly text$ = this.facade.text.asObservable().pipe(
    filter((result): result is GetResultTextDto => !!result),
    map((result) => this.mapTranscriptionToText(result))
  );

  readonly glossary$ = this.facade.text.asObservable().pipe(
    filter((result): result is GetResultTextDto => !!result),
    map((result) => result.glossary)
  );

  constructor(
    @Inject(ResultTextFacadeService)
    private readonly facade: ResultTextFacadeService,
    @Inject(NbDialogService) private readonly dialogService: NbDialogService
  ) {}

  private mapTranscriptionToText(transcriptionArray: GetResultTextDto) {
    return transcriptionArray.result;
  }

  getDefinitonFromGlossary(text: string) {
    return this.glossary$.pipe(map((glossary) => glossary[text]));
  }

  openTooltip(dialog: TemplateRef<any>, text: string) {
    this.getDefinitonFromGlossary(text)
      .pipe(
        tap((definition) =>
          this.dialogService.open(dialog, { context: definition })
        )
      )
      .subscribe();
  }
}
